"""Generate production and dev use-case dashboards from anomaly_rules configuration."""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "grafana" / "dashboards" / "sgp8-ltch-system-gbr.json"

DASHBOARDS = (
    {
        "schema": "sgp7",
        "rule_id": "COOLING-SYSTEM-GBR-TS",
        "uid": "sgp7-cooling-system-gbr",
        "title": "SGP7 Cooling System (COOLING-SYSTEM-GBR-TS)",
        "filename": "sgp7-cooling-system-gbr.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres-prod"},
    },
    {
        "schema": "sgp8",
        "rule_id": "HTCH-SYSTEM-GBR-TS",
        "uid": "sgp8-htch-system-gbr",
        "title": "SGP8 HT-CH System (HTCH-SYSTEM-GBR-TS)",
        "filename": "sgp8-htch-system-gbr.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres-prod"},
    },
    {
        "schema": "sgp7",
        "rule_id": "LTCH-SYSTEM-GBR",
        "uid": "sgp7-ltch-system-gbr",
        "title": "SGP7 LT-CH System (LTCH-SYSTEM-GBR)",
        "filename": "sgp7-ltch-system-gbr.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres-prod"},
    },
    {
        "schema": "sgp8",
        "rule_id": "LTCH-SYSTEM-GBR",
        "uid": "sgp8-ltch-system-gbr",
        "title": "SGP8 LT-CH System (LTCH-SYSTEM-GBR)",
        "filename": "sgp8-ltch-system-gbr.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres-prod"},
    },
    # New Dev Dashboards with TS model
    {
        "schema": "sgp7_dev",
        "rule_id": "LTCH-SYSTEM-GBR-TS",
        "uid": "sgp7-ltch-system-gbr-ts",
        "title": "SGP7 LT-CH System (LTCH-SYSTEM-GBR-TS)",
        "filename": "sgp7-ltch-system-gbr-ts.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres"},
    },
    {
        "schema": "sgp8_dev",
        "rule_id": "LTCH-SYSTEM-GBR-TS",
        "uid": "sgp8-ltch-system-gbr-ts",
        "title": "SGP8 LT-CH System (LTCH-SYSTEM-GBR-TS)",
        "filename": "sgp8-ltch-system-gbr-ts.json",
        "datasource": {"type": "postgres", "uid": "smartdc-postgres"},
    },
)


def sensor_ctes(schema: str, rule_id: str) -> str:
    return f"""WITH rule AS (
  SELECT preprocessing_config::jsonb AS preprocessing_config,
         regexp_split_to_array(replace(asset_ids, ' ', ''), ',')::text[] AS asset_ids,
         regexp_split_to_array(replace(sensor, ' ', ''), ',')::text[] AS target_names
  FROM {schema}.anomaly_rules
  WHERE ruleid = '{rule_id}'
),
targets AS (
  SELECT DISTINCT unnest(target_names) AS sensor_name FROM rule
),
global_names AS (
  SELECT DISTINCT jsonb_array_elements_text(
    COALESCE(preprocessing_config->'global', '[]'::jsonb)
  ) AS sensor_name
  FROM rule
),
asset_extra AS (
  SELECT entry.key AS asset_name,
         jsonb_array_elements_text(entry.value->'sensors') AS sensor_name
  FROM rule,
       LATERAL jsonb_each(
         COALESCE(preprocessing_config->'assets', '{{}}'::jsonb)
       ) AS entry
),
assets AS (
  SELECT am.asset_id, am.asset_name
  FROM {schema}.asset_master am
  JOIN rule r ON am.asset_id = ANY(r.asset_ids)
),
wanted AS (
  SELECT a.asset_id, g.sensor_name
  FROM assets a CROSS JOIN global_names g
  UNION
  SELECT a.asset_id, e.sensor_name
  FROM assets a JOIN asset_extra e ON e.asset_name = a.asset_name
  UNION
  SELECT a.asset_id, t.sensor_name
  FROM assets a CROSS JOIN targets t
),
resolved AS (
  SELECT DISTINCT sm.sensor_id,
         COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||
         COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS label
  FROM wanted w
  JOIN {schema}.sensor_master sm
    ON sm.asset_id = w.asset_id AND sm.sensor_name = w.sensor_name
  JOIN {schema}.asset_master am ON am.asset_id = sm.asset_id
)"""


def run_psql(sql: str, datasource_uid: str) -> str:
    env = os.environ.copy()
    
    if datasource_uid == "smartdc-postgres-prod":
        password = env.get("PG_PROD_PASSWORD") or env.get("PGPASSWORD", "2Tc2AUypdnFr")
        host = env.get("PG_PROD_HOST", "kdch-sg-aiml-postgresql-01-c.postgres.database.azure.com")
        port = env.get("PG_PROD_PORT", "5432")
        user = env.get("PG_PROD_USER", "kdchdb005")
        database = env.get("PG_PROD_DATABASE", "citus")
    else:
        password = env.get("PG_PASSWORD") or env.get("PGPASSWORD", "2Tc2AUypdnFr")
        host = env.get("PG_HOST", "c.kdch-sg-aiml-postgresql-dev-02.postgres.database.azure.com")
        port = env.get("PG_PORT", "5432")
        user = env.get("PG_USER", "kdchdb005")
        database = env.get("PG_DATABASE", "citus")

    env["PGPASSWORD"] = password
    env.setdefault("PGSSLMODE", "require")
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    command = [
        "psql",
        "-h", host,
        "-p", port,
        "-U", user,
        "-d", database,
        "-t",
        "-A",
        "-v",
        "ON_ERROR_STOP=1",
        "-c",
        sql,
    ]
    return subprocess.run(
        command,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def resolve_sensors(schema: str, rule_id: str, datasource_uid: str) -> list[dict[str, str]]:
    sql = (
        sensor_ctes(schema, rule_id)
        + """
SELECT COALESCE(
  jsonb_agg(
    jsonb_build_object('value', sensor_id, 'text', label)
    ORDER BY sensor_id
  ),
  '[]'::jsonb
)::text
FROM resolved;"""
    )
    res = run_psql(sql, datasource_uid)
    return json.loads(res) if res else []


def variable_query(schema: str, rule_id: str) -> str:
    return (
        sensor_ctes(schema, rule_id)
        + """
SELECT sensor_id AS __value, label AS __text
FROM resolved
ORDER BY label"""
    )


def series_query(schema: str, rule_id: str) -> str:
    return f"""WITH has_pred AS (
  SELECT 1
  FROM {schema}.anomaly_predictions p
  WHERE p.sensor_id = '${{sensors}}'
    AND p.use_case = '{rule_id}'
    AND $__timeFilter(p.eventdatetime)
  LIMIT 1
)
SELECT p.eventdatetime AS "time",
       'actual' AS metric,
       p.actual_value::double precision AS value
FROM {schema}.anomaly_predictions p
WHERE p.sensor_id = '${{sensors}}'
  AND p.use_case = '{rule_id}'
  AND $__timeFilter(p.eventdatetime)
  AND EXISTS (SELECT 1 FROM has_pred)
UNION ALL
SELECT p.eventdatetime AS "time",
       'predicted' AS metric,
       p.predicted_value::double precision AS value
FROM {schema}.anomaly_predictions p
WHERE p.sensor_id = '${{sensors}}'
  AND p.use_case = '{rule_id}'
  AND $__timeFilter(p.eventdatetime)
  AND EXISTS (SELECT 1 FROM has_pred)
UNION ALL
SELECT t.eventdatetime AS "time",
       'telemetry' AS metric,
       t.value::double precision AS value
FROM {schema}.telemetry_sensors_1min_agg t
WHERE t.sensorid = '${{sensors}}'
  AND $__timeFilter(t.eventdatetime)
  AND NOT EXISTS (SELECT 1 FROM has_pred)
ORDER BY 1"""


def generate(config: dict[str, str], template: dict) -> None:
    sensors = resolve_sensors(config["schema"], config["rule_id"], config["datasource"]["uid"])
    if not sensors:
        print(f"Warning: No sensors resolved for {config['rule_id']} in {config['schema']}")

    dashboard = copy.deepcopy(template)
    dashboard["id"] = None
    dashboard["uid"] = config["uid"]
    dashboard["title"] = config["title"]
    dashboard["description"] = (
        f"{config['schema'].upper()} {config['rule_id']} trends. All target and "
        "context sensors are selected by default. Each sensor shows use-case-specific "
        "actual and predicted values, with telemetry fallback when no predictions "
        "exist in the selected time range. Default last 24 hours (SGT)."
    )
    dashboard["tags"] = [
        "smart-dc",
        config["schema"],
        config["rule_id"],
        "trends",
    ]
    dashboard["time"] = {"from": "now-24h", "to": "now"}
    dashboard["timezone"] = "Asia/Singapore"
    dashboard["version"] = 1

    panel = dashboard["panels"][0]
    panel["datasource"] = config["datasource"]
    panel["targets"][0]["datasource"] = config["datasource"]
    panel["targets"][0]["rawSql"] = series_query(
        config["schema"], config["rule_id"]
    )

    variable = dashboard["templating"]["list"][0]
    query = variable_query(config["schema"], config["rule_id"])
    variable["datasource"] = config["datasource"]
    variable["query"] = query
    variable["definition"] = query
    variable["current"] = {
        "text": [sensor["text"] for sensor in sensors],
        "value": [sensor["value"] for sensor in sensors],
    }
    variable["options"] = []

    output = ROOT / "grafana" / "dashboards" / config["filename"]
    output.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.name}: {len(sensors)} sensors")


def main() -> None:
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    for config in DASHBOARDS:
        generate(config, template)


if __name__ == "__main__":
    main()

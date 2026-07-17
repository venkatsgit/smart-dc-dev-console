"""Generate production use-case dashboards from anomaly_rules configuration."""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "grafana" / "dashboards" / "LT_CH_SYTEM_SGP8-1784259593666.json"
DATASOURCE = {"type": "postgres", "uid": "smartdc-postgres-prod"}

DASHBOARDS = (
    {
        "schema": "sgp7",
        "rule_id": "COOLING-SYSTEM-GBR",
        "uid": "sgp7-cooling-system-gbr",
        "title": "SGP7 Cooling System (COOLING-SYSTEM-GBR)",
        "filename": "sgp7-cooling-system-gbr.json",
    },
    {
        "schema": "sgp8",
        "rule_id": "HTCH-SYSTEM-GBR",
        "uid": "sgp8-htch-system-gbr",
        "title": "SGP8 HT-CH System (HTCH-SYSTEM-GBR)",
        "filename": "sgp8-htch-system-gbr.json",
    },
    {
        "schema": "sgp7",
        "rule_id": "LTCH-SYSTEM-GBR",
        "uid": "sgp7-ltch-system-gbr",
        "title": "SGP7 LT-CH System (LTCH-SYSTEM-GBR)",
        "filename": "sgp7-ltch-system-gbr.json",
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


def run_psql(sql: str) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = env.get("PG_PROD_PASSWORD") or env.get("PGPASSWORD", "")
    env.setdefault("PGSSLMODE", "require")
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    command = [
        "psql",
        "-h",
        env.get(
            "PG_PROD_HOST",
            "kdch-sg-aiml-postgresql-01-c.postgres.database.azure.com",
        ),
        "-p",
        env.get("PG_PROD_PORT", "5432"),
        "-U",
        env.get("PG_PROD_USER", "kdchdb005"),
        "-d",
        env.get("PG_PROD_DATABASE", "citus"),
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


def resolve_sensors(schema: str, rule_id: str) -> list[dict[str, str]]:
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
    return json.loads(run_psql(sql))


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
    sensors = resolve_sensors(config["schema"], config["rule_id"])
    if not sensors:
        raise RuntimeError(f"No sensors resolved for {config['rule_id']}")

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
    panel["datasource"] = DATASOURCE
    panel["targets"][0]["datasource"] = DATASOURCE
    panel["targets"][0]["rawSql"] = series_query(
        config["schema"], config["rule_id"]
    )

    variable = dashboard["templating"]["list"][0]
    query = variable_query(config["schema"], config["rule_id"])
    variable["datasource"] = DATASOURCE
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

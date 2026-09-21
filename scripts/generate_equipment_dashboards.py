"""Generate SGP7/SGP8 vibration and power dashboards."""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "grafana" / "dashboards" / "sgp8-ltch-system-gbr.json"
DATASOURCE = {"type": "postgres", "uid": "smartdc-postgres-prod"}

SITE_CONFIG = {
    "sgp7": {
        "asset_ids": (
            "'C_100','C_101','C_102','C_103','C_104',"
            "'C_105','C_106','C_107','C_108'"
        ),
        "vibration-acc_filter": (
            "sm.sensor_name IN "
            "('CH-H-A','CH-V-A','CH-CWP-H-A','CH-CWP-V-A',"
            "'CH-CHWP-H-A','CH-CHWP-V-A')"
        ),
        "vibration-vrms-0-1k_filter": (
            "sm.sensor_name IN "
            "('CH-H-VRMS-0-1K','CH-V-VRMS-0-1K',"
            "'CH-CWP-H-VRMS-0-1K','CH-CWP-V-VRMS-0-1K',"
            "'CH-CHWP-H-VRMS-0-1K','CH-CHWP-V-VRMS-0-1K')"
        ),
        "vibration-vrms-1-5k_filter": (
            "sm.sensor_name IN "
            "('CH-H-VRMS-1-5K','CH-V-VRMS-1-5K',"
            "'CH-CWP-H-VRMS-1-5K','CH-CWP-V-VRMS-1-5K',"
            "'CH-CHWP-H-VRMS-1-5K','CH-CHWP-V-VRMS-1-5K')"
        ),
        "ht_system_use_case": "COOLING-SYSTEM-GBR-TS",
    },
    "sgp8": {
        "asset_ids": (
            "'D_100','D_101','D_102','D_103','D_104',"
            "'D_105','D_106','D_110','D_111'"
        ),
        "vibration-acc_filter": (
            "sm.sensor_name ~ "
            "'^(HT|LT)-CH-[0-9]{2}-(H-A|V-A|CWP-H-A|CWP-V-A|"
            "CHWP-H-A|CHWP-V-A)$'"
        ),
        "vibration-vrms-0-1k_filter": (
            "sm.sensor_name ~ "
            "'^(HT|LT)-CH-[0-9]{2}-(H-VRMS-0-1K|V-VRMS-0-1K|"
            "CWP-H-VRMS-0-1K|CWP-V-VRMS-0-1K|"
            "CHWP-H-VRMS-0-1K|CHWP-V-VRMS-0-1K)$'"
        ),
        "vibration-vrms-1-5k_filter": (
            "sm.sensor_name ~ "
            "'^(HT|LT)-CH-[0-9]{2}-(H-VRMS-1-5K|V-VRMS-1-5K|"
            "CWP-H-VRMS-1-5K|CWP-V-VRMS-1-5K|"
            "CHWP-H-VRMS-1-5K|CHWP-V-VRMS-1-5K)$'"
        ),
        "ht_system_use_case": "HTCH-SYSTEM-GBR-TS",
    },
}

DASHBOARDS = (
    {
        "schema": "sgp7",
        "kind": "vibration-acc",
        "uid": "sgp7-vibration-acc",
        "title": "SGP7 Chiller Vibration Acc",
        "filename": "sgp7-vibration-acc.json",
    },
    {
        "schema": "sgp8",
        "kind": "vibration-acc",
        "uid": "sgp8-vibration-acc",
        "title": "SGP8 Chiller Vibration Acc",
        "filename": "sgp8-vibration-acc.json",
    },
    {
        "schema": "sgp7",
        "kind": "vibration-vrms-0-1k",
        "uid": "sgp7-vibration-vrms-0-1k",
        "title": "SGP7 Chiller Vibration Vrms 0-1k",
        "filename": "sgp7-vibration-vrms-0-1k.json",
    },
    {
        "schema": "sgp8",
        "kind": "vibration-vrms-0-1k",
        "uid": "sgp8-vibration-vrms-0-1k",
        "title": "SGP8 Chiller Vibration Vrms 0-1k",
        "filename": "sgp8-vibration-vrms-0-1k.json",
    },
    {
        "schema": "sgp7",
        "kind": "vibration-vrms-1-5k",
        "uid": "sgp7-vibration-vrms-1-5k",
        "title": "SGP7 Chiller Vibration Vrms 1-5k",
        "filename": "sgp7-vibration-vrms-1-5k.json",
    },
    {
        "schema": "sgp8",
        "kind": "vibration-vrms-1-5k",
        "uid": "sgp8-vibration-vrms-1-5k",
        "title": "SGP8 Chiller Vibration Vrms 1-5k",
        "filename": "sgp8-vibration-vrms-1-5k.json",
    },
    {
        "schema": "sgp7",
        "kind": "power",
        "uid": "sgp7-power",
        "title": "SGP7 Chiller Power",
        "filename": "sgp7-power.json",
    },
    {
        "schema": "sgp8",
        "kind": "power",
        "uid": "sgp8-power",
        "title": "SGP8 Chiller Power",
        "filename": "sgp8-power.json",
    },
)


def sensor_filter(schema: str, kind: str) -> str:
    if kind.startswith("vibration"):
        return SITE_CONFIG[schema][f"{kind}_filter"]
    return (
        "sm.sensor_name ~ '^(CH|CWP|CHWP)-KW(_A|_B|-COMBINED|)$'"
    )


def sensor_query(schema: str, kind: str) -> str:
    config = SITE_CONFIG[schema]
    return f"""SELECT sm.sensor_id AS __value,
       COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||
       COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS __text
FROM {schema}.sensor_master sm
JOIN {schema}.asset_master am ON am.asset_id = sm.asset_id
WHERE sm.asset_id IN ({config["asset_ids"]})
  AND {sensor_filter(schema, kind)}
ORDER BY am.asset_name, sm.sensor_name"""


def run_psql(sql: str) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = env.get("PG_PROD_PASSWORD") or env.get("PGPASSWORD", "2Tc2AUypdnFr")
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


def resolve_sensors(schema: str, kind: str) -> list[dict[str, str]]:
    query = sensor_query(schema, kind).replace(
        "SELECT sm.sensor_id AS __value,\n"
        "       COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||\n"
        "       COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS __text",
        "SELECT sm.sensor_id AS value,\n"
        "       COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||\n"
        "       COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS text",
    )
    sql = f"""SELECT COALESCE(
  jsonb_agg(
    jsonb_build_object('value', selected.value, 'text', selected.text)
    ORDER BY selected.text
  ),
  '[]'::jsonb
)::text
FROM ({query}) selected"""
    return json.loads(run_psql(sql))


def vibration_series(schema: str) -> str:
    return f"""SELECT t.eventdatetime AS "time",
       'telemetry' AS metric,
       t.value::double precision AS value
FROM {schema}.telemetry_sensors_1min_agg t
WHERE t.sensorid = '${{sensors}}'
  AND $__timeFilter(t.eventdatetime)
ORDER BY 1"""


def power_series(schema: str) -> str:
    config = SITE_CONFIG[schema]
    return f"""WITH sensor_meta AS (
  SELECT sm.sensor_id,
         CASE WHEN am.asset_name LIKE 'HT-%'
              THEN '{config["ht_system_use_case"]}'
              ELSE 'LTCH-SYSTEM-GBR'
         END AS use_case
  FROM {schema}.sensor_master sm
  JOIN {schema}.asset_master am ON am.asset_id = sm.asset_id
  WHERE sm.sensor_id = '${{sensors}}'
),
has_pred AS (
  SELECT 1
  FROM {schema}.anomaly_predictions p
  JOIN sensor_meta sm
    ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
  WHERE p.sensor_id = sm.sensor_id
    AND $__timeFilter(p.eventdatetime)
  LIMIT 1
)
SELECT p.eventdatetime AS "time",
       'actual' AS metric,
       p.actual_value::double precision AS value
FROM {schema}.anomaly_predictions p
JOIN sensor_meta sm
  ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
WHERE p.sensor_id = '${{sensors}}'
  AND $__timeFilter(p.eventdatetime)
UNION ALL
SELECT p.eventdatetime AS "time",
       'predicted' AS metric,
       p.predicted_value::double precision AS value
FROM {schema}.anomaly_predictions p
JOIN sensor_meta sm
  ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
WHERE p.sensor_id = '${{sensors}}'
  AND $__timeFilter(p.eventdatetime)
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
    schema = config["schema"]
    kind = config["kind"]
    sensors = resolve_sensors(schema, kind)
    if not sensors:
        print(f"  Warning: {config['uid']} resolved no sensors")
        return
    
    print(f"  {config['uid']}: {len(sensors)} sensors")

    dashboard = copy.deepcopy(template)
    dashboard["id"] = None
    dashboard["uid"] = config["uid"]
    dashboard["title"] = config["title"]
    
    if kind == "vibration-acc":
        desc = f"{schema.upper()} vibration trends: horizontal and vertical acceleration sensors for chiller, CWP, and CHWP across nine chillers."
    elif kind == "vibration-vrms-0-1k":
        desc = f"{schema.upper()} vibration trends: horizontal and vertical VRMS 0-1k sensors for chiller, CWP, and CHWP across nine chillers."
    elif kind == "vibration-vrms-1-5k":
        desc = f"{schema.upper()} vibration trends: horizontal and vertical VRMS 1-5k sensors for chiller, CWP, and CHWP across nine chillers."
    else:
        desc = f"{schema.upper()} power trends for chiller, CWP, and CHWP combined kW across seven HT and two LT chillers. Uses prioritized anomaly predictions with telemetry fallback."

    dashboard["description"] = desc
    dashboard["tags"] = ["smart-dc", schema, kind, "chiller"]
    dashboard["time"] = {"from": "now-24h", "to": "now"}
    dashboard["timezone"] = "Asia/Singapore"
    dashboard["version"] = 1

    panel = dashboard["panels"][0]
    panel["datasource"] = DATASOURCE
    
    if kind == "vibration-acc":
        panel_desc = "Horizontal/vertical acceleration from 1-minute telemetry."
    elif kind.startswith("vibration-vrms"):
        panel_desc = f"Horizontal/vertical {kind.split('-')[-2]} {kind.split('-')[-1]} from 1-minute telemetry."
    else:
        panel_desc = "Actual/predicted combined kW when a preferred model is available; otherwise 1-minute telemetry."

    panel["description"] = panel_desc
    panel["targets"][0]["datasource"] = DATASOURCE
    panel["targets"][0]["rawSql"] = (
        vibration_series(schema) if kind.startswith("vibration") else power_series(schema)
    )

    variable = dashboard["templating"]["list"][0]
    query = sensor_query(schema, kind)
    variable["label"] = "Asset | Sensor"
    
    if kind.startswith("vibration"):
        var_desc = "Search and multi-select vibration sensors across nine chillers."
    else:
        var_desc = "Search and multi-select combined kW sensors across nine chillers."

    variable["description"] = var_desc
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

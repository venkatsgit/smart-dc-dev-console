"""Generate site-wide Level Trends dashboards with level-based sensor grouping."""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "grafana" / "dashboards" / "LT_CH_SYTEM_SGP8-1784259593666.json"
DATASOURCE = {"type": "postgres", "uid": "smartdc-postgres-prod"}

CONFIGS = [
    {
        "schema": "sgp7",
        "title": "SGP7 Level Trends",
        "uid": "sgp7-level-trends",
        "filename": "sgp7-level-trends.json",
        "site_id": "7",
    },
    {
        "schema": "sgp8",
        "title": "SGP8 Level Trends",
        "uid": "sgp8-level-trends",
        "filename": "sgp8-level-trends.json",
        "site_id": "8",
    }
]

def run_psql(sql: str) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = env.get("PG_PROD_PASSWORD") or env.get("PGPASSWORD", "2Tc2AUypdnFr")
    env.setdefault("PGSSLMODE", "require")
    command = [
        "psql",
        "-h", env.get("PG_PROD_HOST", "kdch-sg-aiml-postgresql-01-c.postgres.database.azure.com"),
        "-p", env.get("PG_PROD_PORT", "5432"),
        "-U", env.get("PG_PROD_USER", "kdchdb005"),
        "-d", env.get("PG_PROD_DATABASE", "citus"),
        "-t", "-A", "-c", sql,
    ]
    return subprocess.run(command, env=env, check=True, capture_output=True, text=True).stdout.strip()

def get_levels(schema: str, site_id: str) -> list[str]:
    sql = f"SELECT DISTINCT SUBSTRING(ruleid FROM 7 FOR 2) FROM {schema}.anomaly_rules WHERE ruleid LIKE 'KDCS{site_id}-%' AND ruleid LIKE '%-GBR%' ORDER BY 1"
    return run_psql(sql).splitlines()

def generate(config: dict) -> None:
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    levels = get_levels(config["schema"], config["site_id"])
    if not levels:
        print(f"No levels found for {config['schema']}")
        return

    dashboard = copy.deepcopy(template)
    dashboard["uid"] = config["uid"]
    dashboard["title"] = config["title"]
    dashboard["description"] = f"Site-wide {config['schema'].upper()} trends grouped by level. Includes target and context sensors for all GBR use cases matching the selected floor."
    dashboard["tags"] = ["smart-dc", config["schema"], "level", "trends"]
    
    # 1. Level Variable
    level_var = {
        "datasource": DATASOURCE,
        "definition": f"SELECT DISTINCT SUBSTRING(ruleid FROM 7 FOR 2) FROM {config['schema']}.anomaly_rules WHERE ruleid LIKE 'KDCS{config['site_id']}-%' AND ruleid LIKE '%-GBR%' ORDER BY 1",
        "hide": 0,
        "includeAll": False,
        "label": "Level",
        "multi": False,
        "name": "level",
        "options": [],
        "query": f"SELECT DISTINCT SUBSTRING(ruleid FROM 7 FOR 2) FROM {config['schema']}.anomaly_rules WHERE ruleid LIKE 'KDCS{config['site_id']}-%' AND ruleid LIKE '%-GBR%' ORDER BY 1",
        "refresh": 1,
        "regex": "",
        "sort": 0,
        "type": "query"
    }

    # 2. Sensors Variable (Dynamic based on Level)
    sensors_query = f"""
WITH relevant_rules AS (
  SELECT ruleid, preprocessing_config::jsonb as config, 
         sensor as targets,
         asset_ids
  FROM {config['schema']}.anomaly_rules
  WHERE ruleid LIKE 'KDCS{config['site_id']}-' || '${{level}}' || '-ME-' || '%' AND ruleid LIKE '%-GBR%'
),
targets AS (
  SELECT DISTINCT ruleid, unnest(string_to_array(replace(targets, ' ', ''), ',')) AS sensor_name FROM relevant_rules
),
global_names AS (
  SELECT DISTINCT ruleid, jsonb_array_elements_text(COALESCE(config->'global', '[]'::jsonb)) AS sensor_name FROM relevant_rules
),
asset_extra AS (
  SELECT ruleid, entry.key AS asset_name, jsonb_array_elements_text(entry.value->'sensors') AS sensor_name
  FROM relevant_rules, LATERAL jsonb_each(COALESCE(config->'assets', '{{}}'::jsonb)) AS entry
),
assets AS (
  SELECT am.asset_id, am.asset_name, r.ruleid
  FROM {config['schema']}.asset_master am
  JOIN relevant_rules r ON am.asset_id = ANY(string_to_array(replace(r.asset_ids, ' ', ''), ','))
),
wanted AS (
  SELECT sm.sensor_id, am.asset_name, sm.sensor_name
  FROM targets t
  JOIN assets am ON am.ruleid = t.ruleid
  JOIN {config['schema']}.sensor_master sm ON sm.asset_id = am.asset_id AND sm.sensor_name = t.sensor_name
  UNION
  SELECT sm.sensor_id, am.asset_name, sm.sensor_name
  FROM global_names g
  JOIN assets am ON am.ruleid = g.ruleid
  JOIN {config['schema']}.sensor_master sm ON sm.asset_id = am.asset_id AND sm.sensor_name = g.sensor_name
  UNION
  SELECT sm.sensor_id, am.asset_name, sm.sensor_name
  FROM asset_extra ae
  JOIN assets am ON am.ruleid = ae.ruleid AND am.asset_name = ae.asset_name
  JOIN {config['schema']}.sensor_master sm ON sm.asset_id = am.asset_id AND sm.sensor_name = ae.sensor_name
)
SELECT DISTINCT sensor_id AS __value,
       COALESCE(NULLIF(asset_name, ''), sensor_id) || ' | ' || sensor_name AS __text
FROM wanted
ORDER BY 2
"""
    sensors_var = {
        "datasource": DATASOURCE,
        "definition": sensors_query,
        "hide": 0,
        "includeAll": True,
        "allValue": ".*",
        "label": "Asset | Sensor",
        "multi": True,
        "name": "sensors",
        "options": [],
        "query": sensors_query,
        "refresh": 2,
        "regex": "",
        "sort": 1,
        "type": "query",
        "current": {
            "selected": True,
            "text": ["All"],
            "value": ["$__all"]
        }
    }

    dashboard["templating"]["list"] = [level_var, sensors_var]

    # Update Series Query Logic
    series_sql = f"""
WITH sensor_meta AS (
  SELECT sm.sensor_id, r.ruleid as use_case
  FROM {config['schema']}.sensor_master sm
  JOIN {config['schema']}.asset_master am ON am.asset_id = sm.asset_id
  JOIN {config['schema']}.anomaly_rules r ON am.asset_id = ANY(string_to_array(replace(r.asset_ids, ' ', ''), ','))
  WHERE sm.sensor_id = '${{sensors}}'
    AND r.ruleid LIKE 'KDCS{config['site_id']}-' || '${{level}}' || '-ME-' || '%' AND r.ruleid LIKE '%-GBR%'
    AND (
      sm.sensor_name = ANY(string_to_array(replace(r.sensor, ' ', ''), ',')) OR
      sm.sensor_name = ANY(ARRAY(SELECT jsonb_array_elements_text(COALESCE(r.preprocessing_config::jsonb->'global', '[]'::jsonb)))) OR
      EXISTS (
        SELECT 1 FROM jsonb_each(COALESCE(r.preprocessing_config::jsonb->'assets', '{{}}'::jsonb)) as e
        WHERE e.key = am.asset_name AND sm.sensor_name = ANY(ARRAY(SELECT jsonb_array_elements_text(e.value->'sensors')))
      )
    )
),
has_pred AS (
  SELECT 1
  FROM {config['schema']}.anomaly_predictions p
  JOIN sensor_meta sm ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
  WHERE $__timeFilter(p.eventdatetime)
  LIMIT 1
)
SELECT p.eventdatetime AS "time",
       'actual' AS metric,
       p.actual_value::double precision AS value
FROM {config['schema']}.anomaly_predictions p
JOIN sensor_meta sm ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
WHERE $__timeFilter(p.eventdatetime)
UNION ALL
SELECT p.eventdatetime AS "time",
       'predicted' AS metric,
       p.predicted_value::double precision AS value
FROM {config['schema']}.anomaly_predictions p
JOIN sensor_meta sm ON sm.sensor_id = p.sensor_id AND sm.use_case = p.use_case
WHERE $__timeFilter(p.eventdatetime)
UNION ALL
SELECT t.eventdatetime AS "time",
       'telemetry' AS metric,
       t.value::double precision AS value
FROM {config['schema']}.telemetry_sensors_1min_agg t
WHERE t.sensorid = '${{sensors}}'
  AND $__timeFilter(t.eventdatetime)
  AND NOT EXISTS (SELECT 1 FROM has_pred)
ORDER BY 1
"""
    dashboard["panels"][0]["targets"][0]["rawSql"] = series_sql
    dashboard["panels"][0]["datasource"] = DATASOURCE
    dashboard["panels"][0]["title"] = "${sensors:text}"

    output = ROOT / "grafana" / "dashboards" / config["filename"]
    output.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.name}")

def main():
    for config in CONFIGS:
        generate(config)

if __name__ == "__main__":
    main()

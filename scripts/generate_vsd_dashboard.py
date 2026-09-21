"""Generate SGP8 VSD dashboard from sgp8_dev sensor_master (all VSD sensors)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "grafana" / "dashboards" / "sgp8-vsd.json"
DS = {"type": "postgres", "uid": "smartdc-postgres"}
SCHEMA = "sgp8_dev"

SENSORS_Q = f"""SELECT sm.sensor_id AS __value,
       COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||
       COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS __text
FROM {SCHEMA}.sensor_master sm
INNER JOIN {SCHEMA}.asset_master am ON am.asset_id = sm.asset_id
WHERE sm.sensor_name ILIKE '%VSD%'
   OR COALESCE(sm.description, '') ILIKE '%VSD%'
ORDER BY am.asset_name, sm.sensor_name"""

SERIES_SQL = f"""SELECT t.eventdatetime AS "time",
       'telemetry' AS metric,
       t.value::double precision AS value
FROM {SCHEMA}.telemetry_sensors_1min_agg t
WHERE t.sensorid = '${{sensors}}'
  AND '${{source}}' = 'telemetry'
  AND $__timeFilter(t.eventdatetime)
UNION ALL
SELECT p.eventdatetime AS "time",
       'actual (' || p.use_case || ')' AS metric,
       p.actual_value::double precision AS value
FROM {SCHEMA}.anomaly_predictions p
WHERE p.sensor_id = '${{sensors}}'
  AND '${{source}}' = 'anomaly_predictions'
  AND $__timeFilter(p.eventdatetime)
UNION ALL
SELECT p.eventdatetime AS "time",
       'predicted (' || p.use_case || ')' AS metric,
       p.predicted_value::double precision AS value
FROM {SCHEMA}.anomaly_predictions p
WHERE p.sensor_id = '${{sensors}}'
  AND '${{source}}' = 'anomaly_predictions'
  AND $__timeFilter(p.eventdatetime)
ORDER BY 1"""


def run_psql(sql: str) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = env.get("PG_PASSWORD") or env.get(
        "PGPASSWORD", "2Tc2AUypdnFr"
    )
    env.setdefault("PGSSLMODE", "require")
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    command = [
        "psql",
        "-h",
        env.get(
            "PG_HOST",
            "c.kdch-sg-aiml-postgresql-dev-02.postgres.database.azure.com",
        ),
        "-p",
        env.get("PG_PORT", "5432"),
        "-U",
        env.get("PG_USER", "kdchdb005"),
        "-d",
        env.get("PG_DATABASE", "citus"),
        "-t",
        "-A",
        "-v",
        "ON_ERROR_STOP=1",
        "-c",
        sql,
    ]
    return subprocess.run(
        command, env=env, check=True, capture_output=True, text=True
    ).stdout.strip()


def resolve_sensors() -> list[dict[str, str]]:
    sql = f"""
WITH resolved AS (
  SELECT sm.sensor_id,
         COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' ||
         COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS label
  FROM {SCHEMA}.sensor_master sm
  INNER JOIN {SCHEMA}.asset_master am ON am.asset_id = sm.asset_id
  WHERE sm.sensor_name ILIKE '%VSD%'
     OR COALESCE(sm.description, '') ILIKE '%VSD%'
)
SELECT COALESCE(
  jsonb_agg(
    jsonb_build_object('value', sensor_id, 'text', label)
    ORDER BY label
  ),
  '[]'::jsonb
)::text
FROM resolved;
"""
    return json.loads(run_psql(sql) or "[]")


def main() -> None:
    sensors = resolve_sensors()
    if not sensors:
        raise RuntimeError("No VSD sensors resolved in sgp8_dev")

    dashboard = {
        "uid": "sgp8-vsd",
        "title": "SGP8 VSD Trends (Dev)",
        "description": (
            "SGP8_DEV Variable Speed Drive trends for cooling towers and "
            "related pumps. All VSD sensors selected by default. Source "
            "dropdown chooses telemetry or anomaly_predictions directly. "
            "Default last 24 hours (SGT)."
        ),
        "tags": ["smart-dc", "sgp8", "sgp8_dev", "vsd", "trends"],
        "timezone": "Asia/Singapore",
        "schemaVersion": 39,
        "version": 1,
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "links": [],
        "liveNow": False,
        "refresh": "1m",
        "time": {"from": "now-24h", "to": "now"},
        "timepicker": {},
        "weekStart": "",
        "annotations": {"list": []},
        "templating": {
            "list": [
                {
                    "name": "source",
                    "label": "Source",
                    "description": (
                        "Query telemetry_sensors_1min_agg or "
                        "anomaly_predictions directly (no auto-fallback)."
                    ),
                    "type": "custom",
                    "datasource": None,
                    "query": "telemetry,anomaly_predictions",
                    "options": [
                        {
                            "text": "telemetry",
                            "value": "telemetry",
                            "selected": True,
                        },
                        {
                            "text": "anomaly_predictions",
                            "value": "anomaly_predictions",
                        },
                    ],
                    "current": {
                        "text": "telemetry",
                        "value": "telemetry",
                    },
                    "hide": 0,
                    "includeAll": False,
                    "multi": False,
                    "refresh": 1,
                    "skipUrlSync": False,
                },
                {
                    "name": "sensors",
                    "label": "Asset | Sensor",
                    "description": (
                        "All VSD sensors on sgp8_dev Cooling System assets. "
                        "Label: AssetName | SensorName"
                    ),
                    "type": "query",
                    "datasource": DS,
                    "query": SENSORS_Q,
                    "definition": SENSORS_Q,
                    "current": {
                        "text": [s["text"] for s in sensors],
                        "value": [s["value"] for s in sensors],
                    },
                    "hide": 0,
                    "includeAll": False,
                    "multi": True,
                    "refresh": 1,
                    "regex": "",
                    "skipUrlSync": False,
                    "sort": 1,
                    "options": [],
                },
            ]
        },
        "panels": [
            {
                "id": 1,
                "type": "timeseries",
                "title": "${sensors:text}",
                "repeat": "sensors",
                "repeatDirection": "h",
                "maxPerRow": 2,
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 0},
                "datasource": DS,
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "axisBorderShow": False,
                            "axisCenteredZero": False,
                            "axisColorMode": "text",
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "barAlignment": 0,
                            "drawStyle": "line",
                            "fillOpacity": 10,
                            "gradientMode": "none",
                            "lineInterpolation": "linear",
                            "lineWidth": 1,
                            "pointSize": 5,
                            "showPoints": "never",
                            "spanNulls": False,
                            "stacking": {"group": "A", "mode": "none"},
                            "thresholdsStyle": {"mode": "off"},
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "green", "value": None}],
                        },
                        "unit": "none",
                    },
                    "overrides": [],
                },
                "options": {
                    "legend": {
                        "calcs": [],
                        "displayMode": "list",
                        "placement": "bottom",
                        "showLegend": True,
                    },
                    "tooltip": {"mode": "multi", "sort": "none"},
                },
                "targets": [
                    {
                        "refId": "A",
                        "datasource": DS,
                        "editorMode": "code",
                        "format": "time_series",
                        "rawQuery": True,
                        "rawSql": SERIES_SQL,
                    }
                ],
            }
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(sensors)} sensors")


if __name__ == "__main__":
    main()

"""Generate grafana/dashboards/asset-sensor-trends.json"""
from __future__ import annotations

import json
from pathlib import Path

DS = {"type": "postgres", "uid": "smartdc-postgres"}

# Single searchable multi-select: shows "Asset | Sensor", value = sensor_id
SENSORS_Q = (
    "SELECT sm.sensor_id AS __value, "
    "COALESCE(NULLIF(am.asset_name, ''), am.asset_id) || ' | ' || "
    "COALESCE(NULLIF(sm.sensor_name, ''), sm.sensor_id) AS __text "
    "FROM ${schema}.sensor_master sm "
    "INNER JOIN ${schema}.asset_master am ON am.asset_id = sm.asset_id "
    "ORDER BY 2"
)

# Panel repeats on $sensors — each instance is one sensor_id.
SERIES_SQL = """WITH has_pred AS (
  SELECT 1
  FROM ${schema}.anomaly_predictions p
  WHERE p.sensor_id = '${sensors}'
    AND p.use_case LIKE '%-GBR-TS'
    AND $__timeFilter(p.eventdatetime)
  LIMIT 1
)
SELECT p.eventdatetime AS "time",
       'actual' AS metric,
       p.actual_value::double precision AS value
FROM ${schema}.anomaly_predictions p
WHERE p.sensor_id = '${sensors}'
  AND p.use_case LIKE '%-GBR-TS'
  AND $__timeFilter(p.eventdatetime)
  AND EXISTS (SELECT 1 FROM has_pred)
UNION ALL
SELECT p.eventdatetime AS "time",
       'predicted' AS metric,
       p.predicted_value::double precision AS value
FROM ${schema}.anomaly_predictions p
WHERE p.sensor_id = '${sensors}'
  AND p.use_case LIKE '%-GBR-TS'
  AND $__timeFilter(p.eventdatetime)
  AND EXISTS (SELECT 1 FROM has_pred)
UNION ALL
SELECT t.eventdatetime AS "time",
       'telemetry' AS metric,
       t.value::double precision AS value
FROM ${schema}.telemetry_sensors_1min_agg t
WHERE t.sensorid = '${sensors}'
  AND $__timeFilter(t.eventdatetime)
  AND NOT EXISTS (SELECT 1 FROM has_pred)
ORDER BY 1"""


def main() -> None:
    dashboard = {
        "uid": "asset-sensor-trends",
        "title": "Asset / Sensor Trends",
        "description": (
            "Multi-schema trends: one searchable multi-select of Asset | Sensor. "
            "One graph per selected sensor. Anomaly predictions show actual + "
            "predicted; others use telemetry_sensors_1min_agg. "
            "Default last 24 hours (SGT)."
        ),
        "tags": ["smart-dc", "trends"],
        "timezone": "Asia/Singapore",
        "schemaVersion": 39,
        "version": 8,
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
                    "name": "schema",
                    "label": "Schema",
                    "type": "custom",
                    "datasource": None,
                    "query": "sgp7,sgp8,sgp7_dev,sgp8_dev",
                    "options": [
                        {"text": "sgp7", "value": "sgp7"},
                        {"text": "sgp8", "value": "sgp8"},
                        {"text": "sgp7_dev", "value": "sgp7_dev", "selected": True},
                        {"text": "sgp8_dev", "value": "sgp8_dev"},
                    ],
                    "current": {"text": "sgp7_dev", "value": "sgp7_dev"},
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
                        "Type to search. Multi-select sensors across any assets. "
                        "Label format: AssetName | SensorName"
                    ),
                    "type": "query",
                    "datasource": DS,
                    "query": SENSORS_Q,
                    "definition": SENSORS_Q,
                    "current": {},
                    "hide": 0,
                    "includeAll": False,
                    "multi": True,
                    "refresh": 1,
                    "regex": "",
                    "skipUrlSync": False,
                    "sort": 1,
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

    out = Path(__file__).resolve().parents[1] / "grafana" / "dashboards" / "asset-sensor-trends.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

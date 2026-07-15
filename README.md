# smart-dc-dev-console

Local + Kubernetes Grafana for Smart DC developer trends against **`sgp7_dev`**.

## Features

- Searchable multi-select **Asset | Sensor** (across assets)
- One chart per selected sensor (side-by-side layout; editable in Grafana)
- Anomaly predictions → **actual** + **predicted**; otherwise **telemetry_sensors_1min_agg**
- Default range: last **24 hours**, timezone **Asia/Singapore**

## Prerequisites (local)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- Network access to the Smart DC Azure Postgres (Citus) host

## Quick start (local)

1. Copy env and fill Postgres credentials (same values as sibling `smart-dc-anomaly-engine/.devenv`):

   ```powershell
   cd poc\smart-dc-dev-console
   copy .env.example .env
   # Edit .env — set PG_PASSWORD and confirm PG_HOST / PG_USER / PG_DATABASE
   ```

2. Start Grafana:

   ```powershell
   docker compose up -d
   ```

3. Open [http://localhost:3000](http://localhost:3000)  
   Login: `admin` / `admin` (from `.env` by default).

4. Open folder **Smart DC** → dashboard **Asset / Sensor Trends**.

### Using the dashboard

1. Open **Asset | Sensor** and **type to search** (e.g. `HT-CH` or `CHWRT`).
2. Multi-select any sensors — including from different assets.
3. Each selection gets its **own chart** (two per row by default; drag in **Edit** to rearrange).
4. Default range is **Last 24 hours** (timezone **Asia/Singapore**).

## Kubernetes (`smart-dc-dev`)

Follows the same pattern as `smart-dc-mlops/mlflow_deployment`.

- Ingress path: **`/devconsole`** (same nginx host as `/mlflowdev`)
- Grafana data (UI dashboards) on **Azure Disk**; JSON export path on Azure File share `dev-devconsole-grafana`

See **[k8s/README.md](k8s/README.md)** for generate/apply steps.

```powershell
cd poc\smart-dc-dev-console\k8s
python deploy.py
# then kubectl apply -f dev/generated/...
```

Expected URL: `http://4.144.173.96/devconsole`

## Docker image

```powershell
docker build -t aimlsgkdchregistrydev.azurecr.io/smart-dc-dev-console:v1.0.0 .
az acr login --name aimlsgkdchregistrydev
docker push aimlsgkdchregistrydev.azurecr.io/smart-dc-dev-console:v1.0.0
```

## Layout

```
grafana/provisioning/   datasources + dashboard provider
grafana/dashboards/     provisioned JSON dashboards
k8s/                    templates, config, deploy.py, generated/
Dockerfile
docker-compose.yml
.env.example
```

## Notes

- Schema is fixed to **`sgp7_dev`**. Local secrets stay in `.env` (gitignored).
- Rebuild dashboard JSON: `python scripts\generate_dashboard.py`

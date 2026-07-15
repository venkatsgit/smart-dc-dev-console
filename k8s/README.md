# Kubernetes deployment — Smart DC Dev Console (Grafana)

Mirrors [`poc/smart-dc-mlops/mlflow_deployment`](../../smart-dc-mlops/mlflow_deployment): templates → `deploy.py` → `dev/generated/` → `kubectl apply`.

## What gets deployed

| Resource | Name | Notes |
|----------|------|--------|
| Deployment | `grafana-dev` | Image `smart-dc-dev-console`, port 3000 |
| Service | `grafana-service-dev` | ClusterIP |
| Ingress | `grafana-ingress-dev` | Path `/devconsole` (same nginx rewrite/auth as `/mlflowdev`) |
| PVC + PV | `grafana-data-pvc-dev` | **Azure Disk** (`managed-csi`) → `/var/lib/grafana` (sqlite + UI dashboards) |
| PVC + PV | `grafana-dashboards-pvc-dev` | **Azure File** share `dev-devconsole-grafana` → `/var/lib/grafana/dashboards-export` |
| Secrets | `grafana-postgres-secret-dev`, `grafana-admin-secret-dev` | Datasource + admin login |

**Namespace:** `smart-dc-dev`

**Persistence:** Grafana’s database and UI-created dashboards live on Azure Disk (SQLite cannot run reliably on Azure File due to locking). The file share is mounted for JSON exports under `dashboards-export`.

## Prerequisites

1. AKS access (`kubectl` context to `sgkdchaksdev01`).
2. Azure File share **`dev-devconsole-grafana`** must exist (used for `dashboards-export`; cluster secret `azure-secret`).
3. Build and push the Grafana image:

   ```powershell
   cd poc\smart-dc-dev-console
   docker build -t aimlsgkdchregistrydev.azurecr.io/smart-dc-dev-console:v1.0.0 .
   az acr login --name aimlsgkdchregistrydev
   docker push aimlsgkdchregistrydev.azurecr.io/smart-dc-dev-console:v1.0.0
   ```

4. Ingress basic auth secret `basic-auth-secret` already present (shared with MLflow).

## Generate + apply

```powershell
cd poc\smart-dc-dev-console\k8s
python deploy.py

kubectl apply -f dev/generated/grafana-postgres-secret.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-admin-secret.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-pv.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-pvc.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-deployment.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-service.yaml --insecure-skip-tls-verify
kubectl apply -f dev/generated/grafana-ingress.yaml --insecure-skip-tls-verify
```

Or: `bash deploy.sh` (Git Bash / WSL).

## Access

Same ingress LB as MLflow:

```text
http://4.144.173.96/devconsole
```

1. Nginx basic auth (same as MLflow)
2. Grafana login (`GF_SECURITY_ADMIN_*` from config)

## Config

Edit [`dev/devconsole-dev-config.yaml`](dev/devconsole-dev-config.yaml), then re-run `python deploy.py` and re-apply.

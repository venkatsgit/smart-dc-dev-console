#!/usr/bin/env bash
# Apply generated Grafana / Dev Console manifests to the cluster.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATED="${SCRIPT_DIR}/dev/generated"
NS=smart-dc-dev

echo "Generating manifests..."
python "${SCRIPT_DIR}/deploy.py"

echo "Applying secrets, PV, PVC..."
kubectl apply -f "${GENERATED}/grafana-postgres-secret.yaml" --insecure-skip-tls-verify
kubectl apply -f "${GENERATED}/grafana-admin-secret.yaml" --insecure-skip-tls-verify
kubectl apply -f "${GENERATED}/grafana-pv.yaml" --insecure-skip-tls-verify
kubectl apply -f "${GENERATED}/grafana-pvc.yaml" --insecure-skip-tls-verify

echo "Applying Deployment, Service, Ingress..."
kubectl apply -f "${GENERATED}/grafana-deployment.yaml" --insecure-skip-tls-verify
kubectl apply -f "${GENERATED}/grafana-service.yaml" --insecure-skip-tls-verify
kubectl apply -f "${GENERATED}/grafana-ingress.yaml" --insecure-skip-tls-verify

echo "Done. Check: kubectl get pods,svc,ing -n ${NS} -l app=grafana --insecure-skip-tls-verify"
echo "URL: http://<ingress-ip>/devconsole"

#!/usr/bin/env python3
"""Generate smart-dc-dev-console Kubernetes manifests from templates + config."""

from __future__ import annotations

import base64
from pathlib import Path
from string import Template

import yaml


def load_config(config_file: Path) -> dict:
    with open(config_file, encoding="utf-8") as f:
        return yaml.safe_load(f)


def b64(value) -> str:
    if isinstance(value, int):
        value = str(value)
    return base64.b64encode(str(value).encode()).decode()


def process_template(template_file: Path, config: dict, output_file: Path) -> None:
    template = Template(template_file.read_text(encoding="utf-8"))
    substitutions = {k: (str(v) if v is not None else "") for k, v in config.items()}

    substitutions["PG_USER_B64"] = b64(config["PG_USER"])
    substitutions["PG_PASSWORD_B64"] = b64(config["PG_PASSWORD"])
    substitutions["PG_HOST_B64"] = b64(config["PG_HOST"])
    substitutions["PG_DATABASE_B64"] = b64(config["PG_DATABASE"])
    substitutions["PG_PORT_B64"] = b64(config["PG_PORT"])
    substitutions["GF_SECURITY_ADMIN_USER_B64"] = b64(config["GF_SECURITY_ADMIN_USER"])
    substitutions["GF_SECURITY_ADMIN_PASSWORD_B64"] = b64(config["GF_SECURITY_ADMIN_PASSWORD"])

    output_file.write_text(template.substitute(substitutions), encoding="utf-8")
    print(f"Generated: {output_file}")


def main() -> None:
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    config_files = list(script_dir.rglob("devconsole-*-config.yaml"))

    if not config_files:
        print("No devconsole-*-config.yaml files found")
        return

    templates = [
        "grafana-deployment-template.yaml",
        "grafana-service-template.yaml",
        "grafana-pv-template.yaml",
        "grafana-pvc-template.yaml",
        "grafana-dashboards-pvc-template.yaml",
        "grafana-postgres-secret-template.yaml",
        "grafana-admin-secret-template.yaml",
        "grafana-ingress-template.yaml",
    ]

    for config_file in config_files:
        print(f"\nProcessing: {config_file.relative_to(script_dir)}")
        config = load_config(config_file)
        print(f"  Environment: {config.get('ENVIRONMENT')}")
        print(f"  Namespace: {config.get('NAMESPACE')}")
        print(f"  Path: {config.get('DEVCONSOLE_PATH')}")
        print(f"  File share: {config.get('FILESHARE_NAME')}")

        output_dir = config_file.parent / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)

        for name in templates:
            process_template(
                templates_dir / name,
                config,
                output_dir / name.replace("-template", ""),
            )


if __name__ == "__main__":
    main()

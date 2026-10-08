"""One-shot inventory of the five-file R2F family for a case."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from inspect_csv import summarize_csv
from inspect_manifest import load_manifest
from r2f_case import DEFAULT_CASE, R2FCase, parse_case_id


def print_inventory(case: R2FCase) -> None:
    print("=" * 72)
    print(f"R2F case inventory: {case.case_id}")
    print("=" * 72)
    files = case.files()
    missing = case.missing()
    for name, path in files.items():
        status = "OK" if path.is_file() else "MISSING"
        size = path.stat().st_size if path.is_file() else 0
        print(f"  [{status}] {name:14}  {path.name}  ({size:,} bytes)")
    if missing:
        print(f"Missing files: {missing}")
        return

    manifest = load_manifest(case.manifest)
    scenario = manifest.get("scenario", {})
    counts = manifest.get("counts", {})
    print()
    print(f"Scenario: {scenario.get('name')}  fault={scenario.get('fault')}  load={scenario.get('load')}")
    print(f"Counts:   {json.dumps(counts)}")
    print()
    print("File roles (product view):")
    print("  manifest.json     contract + QC for the run")
    print("  sensors.csv       site-lookalike BMS tags (what a detector would see)")
    print("  twin_sensors.csv  twin native tags (SI-ish, from sensor_schema)")
    print("  truth.csv         hidden physics + labels (not on the plant bus)")
    print("  cascade.csv       which tags departed the healthy band, and in what order")


def main(argv: list[str]) -> int:
    if argv and argv[0] in {"-h", "--help"}:
        print("Usage: python summarize_run.py [case_id] [--csv]")
        print(f"Default case: {DEFAULT_CASE}")
        return 0
    case_id = parse_case_id(argv)
    case = R2FCase(case_id)
    print_inventory(case)
    if "--csv" in argv:
        for name, path in case.files().items():
            if name == "manifest" or not path.is_file():
                continue
            print()
            summarize_csv(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

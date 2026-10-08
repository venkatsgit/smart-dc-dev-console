"""Print a product-manager summary of one R2F manifest.json."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from r2f_case import DEFAULT_CASE, R2FCase, parse_case_id


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def hours(seconds: float | None) -> str:
    if seconds is None:
        return "n/a"
    return f"{seconds / 3600:.1f} h ({seconds:.0f} s)"


def pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{100.0 * value:.2f}%"


def print_section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def summarize(manifest: dict, path: Path) -> None:
    model = manifest.get("model", {})
    scenario = manifest.get("scenario", {})
    run = scenario.get("run", {})
    boundary = scenario.get("boundary_profile", {})
    anchor = scenario.get("severity_anchor", {})
    counts = manifest.get("counts", {})
    settle = manifest.get("settle", {})
    solver = manifest.get("solver", {})
    conservation = manifest.get("conservation", {})
    background = manifest.get("background", {})
    cascade = manifest.get("cascade", {})
    files = manifest.get("files", {})

    print_section("1. What this file is")
    print(f"Path:     {path.name}")
    print(f"Schema:   {manifest.get('$schema')}")
    print("Role:     Lab notebook for one physics twin run (inputs + QC + file map).")

    print_section("2. Which machine and operating point")
    print(f"Model id:     {model.get('id')}")
    print(f"Model name:   {model.get('name')}")
    print(f"Version:      {model.get('version')}")
    print(f"Graph hash:   {model.get('graph_hash')}")
    print(f"Refrigerant:  {model.get('refrigerant')}")
    print(f"Chillers:     {', '.join(model.get('chillers') or [])}")
    topology = model.get("topology", {})
    print(
        "Topology:     "
        f"{topology.get('chillers')} chiller, "
        f"{topology.get('nodes')} nodes, "
        f"{topology.get('edges')} edges, loops={topology.get('loops')}"
    )

    print_section("3. What experiment was run")
    print(f"Case id:      {scenario.get('id')}")
    print(f"Name:         {scenario.get('name')}")
    print(f"Fault id:     {scenario.get('fault')}")
    print(f"Load point:   {scenario.get('load')}")
    print(f"Chiller:      {scenario.get('chiller')}")
    print(f"Boundary:     {boundary.get('id')} — {boundary.get('name')} ({boundary.get('day')})")
    detail = boundary.get("detail") or ""
    if detail:
        print(f"Day story:    {detail}")
    print(f"Onset:        {hours(scenario.get('onset_s'))}  (start of faulted day)")
    print(f"Baseline:     {hours(run.get('baseline_s'))}")
    print(f"Fault window: {hours(run.get('duration_s'))}")
    print(f"Settle:       {hours(run.get('settle_s'))}")
    print(f"Sample:       every {run.get('sample_interval_s')} s")
    print(f"Stop on:      {run.get('stop_on')}")
    print(f"Seed:         {manifest.get('seed', run.get('seed'))}")

    profile = scenario.get("severity_profile", {})
    print()
    print("Severity profile (how the fault is injected):")
    print(f"  kind:            {profile.get('kind')}")
    print(f"  profile onset:   {hours(profile.get('onset_s'))}  (0 = start of the faulted day)")
    print(f"  duration:        {hours(profile.get('duration_s'))}")
    print(f"  final_severity:  {profile.get('final_severity')}")
    print(f"  target_scale:    {scenario.get('target_scale')}")

    print()
    print("Physical anchor (what SL1 means on this machine):")
    print(f"  standard:        {anchor.get('standard')}")
    print(f"  level:           {anchor.get('level')}")
    print(f"  surface_loss:    {pct(anchor.get('surface_loss'))} of tube surface")
    print(f"  R_f:             {anchor.get('R_f_K_per_W')} K/W")
    print(f"  UA clean:        {anchor.get('UA_clean_W_per_K')} W/K")
    print(f"  UA fouled:       {anchor.get('UA_fouled_W_per_K')} W/K")
    print(f"  note:            {anchor.get('note')}")

    print_section("4. Fault catalogue entry (what we expect to see)")
    defs = manifest.get("fault_definitions") or []
    if not defs:
        print("No fault_definitions in this manifest.")
    for item in defs:
        print(f"Instance:   {item.get('instance')}")
        print(f"Id:         {item.get('id')}")
        print(f"Name:       {item.get('name')}")
        print(f"Category:   {item.get('category')}")
        print(f"Terminal:   {item.get('terminal')}")
        print(f"TTF hours:  {item.get('typical_ttf_h')}")
        print()
        print("Mechanism:")
        print(f"  {item.get('mechanism')}")
        print()
        print("Expected signature (physics order):")
        for row in item.get("signature") or []:
            print(
                f"  order {row.get('order')}: {row.get('signal'):16} "
                f"{row.get('direction'):4}  — {row.get('note')}"
            )

    print_section("5. Output contracts (what the CSVs contain)")
    schema = manifest.get("sensor_schema") or []
    keppel = manifest.get("keppel_tags") or []
    truth_cols = manifest.get("truth_columns") or []
    print(f"Twin sensor tags (sensor_schema / twin_sensors.csv): {len(schema)}")
    kinds = Counter(row.get("kind") for row in schema)
    print("  kinds:", dict(kinds))
    print(f"Site-style tags (keppel_tags / sensors.csv):         {len(keppel)}")
    print("  classes:", dict(Counter(row.get("class") for row in keppel)))
    print(f"Truth columns (truth.csv):                          {len(truth_cols)}")
    print("  roles:", dict(Counter(row.get("role") for row in truth_cols)))
    print("Row counts from run:", dict(counts))

    print_section("6. Did the run complete cleanly?")
    print(f"Settle converged:  {settle.get('converged')}  residual={settle.get('residual_K_per_s')}")
    print(f"Events:            {manifest.get('events')}")
    print(f"Terminal event:    {manifest.get('terminal_event')}")
    print(f"Warnings:          {manifest.get('warnings')}")
    print(
        "Solver:            "
        f"steps={solver.get('steps')}, wall={solver.get('wall_time_s')} s, "
        f"speedup={solver.get('realtime_speedup')}x, "
        f"hydraulic non-converged={solver.get('hydraulic_non_converged_samples')}"
    )
    energy = conservation.get("energy_chiller_relative", {})
    rejection = conservation.get("energy_rejection_relative", {})
    print(
        "Conservation:      "
        f"chiller energy mean={energy.get('mean')}, max={energy.get('max')}; "
        f"rejection mean={rejection.get('mean')}, max={rejection.get('max')}; "
        f"refrigerant drift={conservation.get('refrigerant_mass_relative_drift')}"
    )

    print_section("7. Signature check (did physics move the right way?)")
    checks = manifest.get("signature_check") or []
    agree = sum(1 for row in checks if row.get("agrees"))
    print(f"{agree}/{len(checks)} expected directions matched.")
    for row in checks:
        flag = "OK " if row.get("agrees") else "GAP"
        print(
            f"  [{flag}] {row.get('signal'):16}  "
            f"expected {row.get('expected'):6}  observed {row.get('observed'):6}  "
            f"rel_change={row.get('relative_change')}"
        )
        if not row.get("agrees"):
            print(f"         note: {row.get('note')}")

    print_section("8. Cascade digest (first tags that left the healthy band)")
    first = cascade.get("first_departure") or {}
    print(f"First departure:   {first.get('tag')} at +{first.get('minutes_after_onset')} min after onset")
    print(f"Tags departed:     {cascade.get('tags_departed')}")
    print(f"Predicted agree:   {cascade.get('predicted_agree')}")
    print(f"Predicted disagree:{cascade.get('predicted_disagree')}")
    print(f"Window (minutes):  {cascade.get('window_min')}")
    print("Observed order:")
    for i, tag in enumerate(cascade.get("order_observed") or [], start=1):
        print(f"  {i}. {tag}")
    test = cascade.get("departure_test") or {}
    if test:
        print("Departure test:", test)

    print_section("9. Background and sibling files")
    filled = background.get("plant_tags_filled_from_80pct_day") or []
    print(f"Background day:    {background.get('day')}  file={background.get('file')}")
    print(f"Plant tags filled from 80% day (not on this 58% export): {len(filled)}")
    print("Sibling files (export-time paths; local copies live next to this JSON):")
    for key, value in files.items():
        print(f"  {key:18} {Path(value).name}")


def main(argv: list[str]) -> int:
    case_id = parse_case_id(argv)
    if argv and argv[0] in {"-h", "--help"}:
        print("Usage: python inspect_manifest.py [case_id]")
        print(f"Default case: {DEFAULT_CASE}")
        return 0
    case = R2FCase(case_id)
    if not case.manifest.is_file():
        print(f"Manifest not found: {case.manifest}", file=sys.stderr)
        return 1
    summarize(load_manifest(case.manifest), case.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

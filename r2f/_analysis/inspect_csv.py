"""Summarize one R2F CSV: shape, time span, missing cells, numeric ranges."""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

from r2f_case import DEFAULT_CASE, R2FCase, parse_case_id

TIME_COLUMNS = ("Event time", "time_s", "departs_at", "scenario_time_s")


def _to_float(value: str) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if math.isnan(number):
        return None
    return number


def summarize_csv(path: Path, sample_cols: int = 12) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            print(f"{path.name}: empty file")
            return
        rows = list(reader)

    print("=" * 72)
    print(path.name)
    print("=" * 72)
    print(f"Rows (data):   {len(rows)}")
    print(f"Columns:       {len(header)}")
    print(f"First columns: {header[:sample_cols]}")
    if len(header) > sample_cols:
        print(f"  ... +{len(header) - sample_cols} more")

    for name in TIME_COLUMNS:
        if name not in header:
            continue
        idx = header.index(name)
        values = [row[idx] for row in rows if idx < len(row) and row[idx].strip()]
        if not values:
            print(f"{name}: (all empty)")
            continue
        print(f"{name}: {values[0]}  →  {values[-1]}  (n={len(values)})")

    empty = []
    numeric_preview = []
    for col_i, name in enumerate(header):
        blanks = 0
        nums: list[float] = []
        non_numeric = 0
        for row in rows:
            cell = row[col_i] if col_i < len(row) else ""
            if cell.strip() == "":
                blanks += 1
                continue
            number = _to_float(cell)
            if number is None:
                non_numeric += 1
            else:
                nums.append(number)
        if blanks:
            empty.append((name, blanks))
        if nums and len(numeric_preview) < 8 and name not in TIME_COLUMNS:
            numeric_preview.append(
                (name, min(nums), max(nums), sum(nums) / len(nums), blanks)
            )

    if empty:
        print(f"Columns with blanks: {len(empty)}")
        for name, blanks in empty[:15]:
            print(f"  {name}: {blanks}/{len(rows)} empty")
        if len(empty) > 15:
            print(f"  ... +{len(empty) - 15} more")
    else:
        print("Columns with blanks: 0")

    if numeric_preview:
        print("Numeric preview (first numeric columns):")
        for name, lo, hi, mean, blanks in numeric_preview:
            print(f"  {name}: min={lo:.6g}  max={hi:.6g}  mean={mean:.6g}  empty={blanks}")

    # Cascade-specific: rows that actually departed
    if "kind" in header and "departs_at_min" in header:
        kind_i = header.index("kind")
        dep_i = header.index("departs_at_min")
        when_i = header.index("departs_at") if "departs_at" in header else None
        tag_i = header.index("tag") if "tag" in header else None
        kinds: dict[str, int] = {}
        departed = []
        for row in rows:
            kind = row[kind_i] if kind_i < len(row) else ""
            kinds[kind] = kinds.get(kind, 0) + 1
            if dep_i < len(row) and row[dep_i].strip():
                tag = row[tag_i] if tag_i is not None and tag_i < len(row) else "?"
                when = row[when_i] if when_i is not None and when_i < len(row) else ""
                departed.append((row[dep_i], tag, when))
        print(f"kind counts: {kinds}")
        if departed:
            departed.sort(key=lambda item: float(item[0]) if _to_float(item[0]) is not None else 1e12)
            print(f"Departed tags: {len(departed)}")
            for minute, tag, when in departed:
                print(f"  +{minute} min  {tag}  {when}")


def main(argv: list[str]) -> int:
    if argv and argv[0] in {"-h", "--help"}:
        print("Usage: python inspect_csv.py [case_id] [sensors|twin_sensors|truth|cascade|all]")
        print(f"Default: {DEFAULT_CASE} all")
        return 0

    case_id = parse_case_id(argv)
    which = argv[1] if len(argv) > 1 else "all"
    case = R2FCase(case_id)
    mapping = {
        "sensors": case.sensors,
        "twin_sensors": case.twin_sensors,
        "truth": case.truth,
        "cascade": case.cascade,
    }
    targets = list(mapping.values()) if which == "all" else [mapping[which]]
    missing = [path for path in targets if not path.is_file()]
    if missing:
        for path in missing:
            print(f"Missing: {path}", file=sys.stderr)
        return 1
    for path in targets:
        summarize_csv(path)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

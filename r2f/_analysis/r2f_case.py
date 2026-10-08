"""Resolve paths for one R2F export case (five-file family)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

R2F_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = Path(__file__).resolve().parent
DEFAULT_CASE = "cond_fouling_SL1_80pct"

SUFFIXES = {
    "manifest": "_manifest.json",
    "sensors": "_sensors.csv",
    "twin_sensors": "_twin_sensors.csv",
    "truth": "_truth.csv",
    "cascade": "_cascade.csv",
}


def load_folder_for_case(case_id: str) -> Path:
    """Return r2f/58 or r2f/80 from the case id suffix."""
    if case_id.endswith("_80pct") or "_80pct_" in case_id:
        return R2F_DIR / "80"
    if case_id.endswith("_58pct") or "_58pct_" in case_id:
        return R2F_DIR / "58"
    # Fallbacks if someone passes a bare id
    for folder in ("80", "58"):
        candidate = R2F_DIR / folder
        if (candidate / f"{case_id}_manifest.json").is_file():
            return candidate
    return R2F_DIR


@dataclass(frozen=True)
class R2FCase:
    case_id: str
    r2f_dir: Path | None = None

    def __post_init__(self) -> None:
        if self.r2f_dir is None:
            object.__setattr__(self, "r2f_dir", load_folder_for_case(self.case_id))

    @property
    def manifest(self) -> Path:
        return self.r2f_dir / f"{self.case_id}{SUFFIXES['manifest']}"

    @property
    def sensors(self) -> Path:
        return self.r2f_dir / f"{self.case_id}{SUFFIXES['sensors']}"

    @property
    def twin_sensors(self) -> Path:
        return self.r2f_dir / f"{self.case_id}{SUFFIXES['twin_sensors']}"

    @property
    def truth(self) -> Path:
        return self.r2f_dir / f"{self.case_id}{SUFFIXES['truth']}"

    @property
    def cascade(self) -> Path:
        return self.r2f_dir / f"{self.case_id}{SUFFIXES['cascade']}"

    def files(self) -> dict[str, Path]:
        return {
            "manifest": self.manifest,
            "sensors": self.sensors,
            "twin_sensors": self.twin_sensors,
            "truth": self.truth,
            "cascade": self.cascade,
        }

    def missing(self) -> list[str]:
        return [name for name, path in self.files().items() if not path.is_file()]


def parse_case_id(argv: list[str], default: str = DEFAULT_CASE) -> str:
    if not argv:
        return default
    if argv[0] in {"-h", "--help"}:
        return default
    return argv[0]

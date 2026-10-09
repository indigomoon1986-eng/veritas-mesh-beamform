"""Shared config and command types for the Veritas beamform stack."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "node.yaml"


def load_config(path: Path | None = None) -> dict[str, Any]:
    with open(path or DEFAULT_CONFIG, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@dataclass
class SteerCommand:
    azimuth_deg: float
    elevation_deg: float = 0.0
    freq_hz: float | None = None
    mode: str = "mrt"
    source: str = "local"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TuneCommand:
    freq_hz: float
    amplitude: float = 0.5
    source: str = "local"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ElementState:
    element_id: int
    phase_deg: float
    amp: float
    nco_word: int
    varactor_word: int
    relay: int


@dataclass
class Plan:
    freq_hz: float
    azimuth_deg: float
    elevation_deg: float
    mode: str
    elements: list[ElementState] = field(default_factory=list)
    weights_re: list[float] = field(default_factory=list)
    weights_im: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "freq_hz": self.freq_hz,
            "azimuth_deg": self.azimuth_deg,
            "elevation_deg": self.elevation_deg,
            "mode": self.mode,
            "weights_re": self.weights_re,
            "weights_im": self.weights_im,
            "elements": [asdict(e) for e in self.elements],
        }

"""RF control layer. Phase law: phi = -2 * pi * freq * dot(r, u) / c."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from app.types import ElementState, Plan, SteerCommand, TuneCommand

C = 299_792_458.0


def look_vector(azimuth_deg: float, elevation_deg: float) -> np.ndarray:
    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    return np.array([math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el)])


def steering_phases(elements: list[dict], freq_hz: float, azimuth_deg: float, elevation_deg: float) -> np.ndarray:
    u = look_vector(azimuth_deg, elevation_deg)
    phases = []
    for el in elements:
        r = np.array([el["x"], el["y"], el["z"]], dtype=float)
        phases.append(-2.0 * math.pi * freq_hz * float(np.dot(r, u)) / C)
    return np.array(phases)


def nco_word(freq_hz: float, clock_hz: float, width: int = 32) -> int:
    return int(round(freq_hz / clock_hz * (1 << width))) & ((1 << width) - 1)


class RfPlanner:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.elements = cfg["array"]["elements"]
        self.freq = float(cfg["array"]["frequency_hz"])
        self.clock = float(cfg["fpga"]["sample_clock_hz"])
        self.channel = None

    def set_channel(self, H: np.ndarray) -> None:
        self.channel = np.asarray(H, dtype=complex)

    def steer(self, cmd: SteerCommand) -> Plan:
        freq = float(cmd.freq_hz or self.freq)
        phases = steering_phases(self.elements, freq, cmd.azimuth_deg, cmd.elevation_deg)
        weights = np.exp(1j * phases)
        if cmd.mode == "zf" and self.channel is not None:
            weights = self._zf(self.channel)
        weights = weights / (np.linalg.norm(weights) + 1e-12)
        return self._plan(freq, cmd.azimuth_deg, cmd.elevation_deg, cmd.mode, weights)

    def tune(self, cmd: TuneCommand) -> Plan:
        self.freq = float(cmd.freq_hz)
        weights = np.ones(len(self.elements), dtype=complex) * float(cmd.amplitude)
        return self._plan(self.freq, 0.0, 0.0, "tune", weights)

    def _zf(self, H: np.ndarray) -> np.ndarray:
        gram = H @ H.conj().T
        w = H.conj().T @ np.linalg.pinv(gram)
        return w[:, 0]

    def _plan(self, freq, az, el, mode, weights) -> Plan:
        states = []
        for i, elem in enumerate(self.elements):
            w = weights[i]
            states.append(ElementState(int(elem["id"]), math.degrees(float(np.angle(w))), float(min(1.0, abs(w))), nco_word(freq, self.clock), int(min(1.0, abs(w)) * 4095), self._band(freq)))
        return Plan(freq, az, el, mode, states, weights.real.tolist(), weights.imag.tolist())

    def _band(self, freq: float) -> int:
        for band in self.cfg["hal"]["lc_bands"]:
            if band["hz_min"] <= freq <= band["hz_max"]:
                return int(band["relay"])
        return 0

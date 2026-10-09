"""Closed loop. Measured phase error trims the next weights."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from app.types import Plan
from fpga.spi_bridge import FpgaBridge
from rf.planner import RfPlanner


class FeedbackLoop:
    def __init__(self, cfg: dict[str, Any], planner: RfPlanner, fpga: FpgaBridge):
        self.gain = float(cfg["feedback"]["phase_gain"])
        self.max_step = math.radians(float(cfg["feedback"]["max_step_deg"]))
        self.planner = planner
        self.fpga = fpga

    def correct(self, plan: Plan, measured_phase_deg: list[float]) -> Plan:
        weights = np.array(plan.weights_re) + 1j * np.array(plan.weights_im)
        for i, meas in enumerate(measured_phase_deg[: len(weights)]):
            planned = math.degrees(math.atan2(plan.weights_im[i], plan.weights_re[i]))
            err = math.radians((meas - planned + 180) % 360 - 180)
            err = max(-self.max_step, min(self.max_step, err))
            weights[i] *= np.exp(-1j * self.gain * err)
        weights = weights / (np.linalg.norm(weights) + 1e-12)
        return self.planner._plan(plan.freq_hz, plan.azimuth_deg, plan.elevation_deg, plan.mode + "+fb", weights)

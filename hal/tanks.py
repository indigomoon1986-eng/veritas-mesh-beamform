"""Varactor codes and band relays. Dry-run until GPIO exists."""

from __future__ import annotations

from typing import Any

from app.types import Plan


class TankHal:
    def __init__(self, cfg: dict[str, Any], dry_run: bool = True):
        self.cfg = cfg
        self.dry_run = dry_run
        self.last: dict[str, Any] = {}

    def apply(self, plan: Plan) -> dict[str, Any]:
        relays = self.cfg["hal"]["relay_gpio"]
        band = plan.elements[0].relay if plan.elements else 0
        gpio_state = {pin: int(i == band) for i, pin in enumerate(relays)}
        varactors = {e.element_id: e.varactor_word for e in plan.elements}
        self.last = {"gpio": gpio_state, "varactor": varactors, "band": band, "dry_run": self.dry_run}
        return self.last

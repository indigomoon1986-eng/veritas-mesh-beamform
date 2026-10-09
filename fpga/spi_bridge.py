"""Host side of the FPGA register map. Dry-runs if SPI is absent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.types import Plan

REG_CONTROL = 0x00
REG_FREQ = 0x04
REG_W_RE = 0x10
REG_W_IM = 0x14
SCALE = 32767


class FpgaBridge:
    def __init__(self, cfg: dict[str, Any], dry_run: bool = True):
        self.cfg = cfg
        self.dry_run = dry_run
        self.device = cfg["fpga"].get("spi_device", "/dev/spidev0.0")
        self.last_write: list[tuple[int, int]] = []
        self._spi = None
        if not dry_run and Path(self.device).exists():
            self._open()

    def _open(self) -> None:
        try:
            import spidev
            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = int(self.cfg["fpga"].get("spi_speed_hz", 8_000_000))
            self._spi = spi
            self.dry_run = False
        except Exception:
            self.dry_run = True

    def push_plan(self, plan: Plan) -> list[tuple[int, int]]:
        words = [(REG_CONTROL, 0x1)]
        if plan.elements:
            words.append((REG_FREQ, plan.elements[0].nco_word & 0xFFFFFFFF))
        for i in range(min(4, len(plan.elements))):
            re = int(max(-1.0, min(1.0, plan.weights_re[i])) * SCALE) & 0xFFFF
            im = int(max(-1.0, min(1.0, plan.weights_im[i])) * SCALE) & 0xFFFF
            words.append((REG_W_RE + 8 * i, re))
            words.append((REG_W_IM + 8 * i, im))
        words.append((REG_CONTROL, 0x2))
        self.last_write = words
        return words

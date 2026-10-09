"""Application layer. Turns a steer or tune request into a mesh packet and an FPGA plan."""

from __future__ import annotations

import json
from pathlib import Path

from app.types import Plan, SteerCommand, TuneCommand, load_config
from feedback.loop import FeedbackLoop
from fpga.spi_bridge import FpgaBridge
from hal.tanks import TankHal
from mesh.protocol import MeshPacket, dumps
from rf.planner import RfPlanner


class BeamApp:
    def __init__(self, config_path: Path | None = None, dry_run: bool = True):
        self.cfg = load_config(config_path)
        self.planner = RfPlanner(self.cfg)
        self.fpga = FpgaBridge(self.cfg, dry_run=dry_run)
        self.hal = TankHal(self.cfg, dry_run=dry_run)
        self.loop = FeedbackLoop(self.cfg, self.planner, self.fpga)
        self.last_plan: Plan | None = None

    def steer(self, cmd: SteerCommand) -> dict:
        plan = self.planner.steer(cmd)
        return self._commit(plan, kind="steer", payload=cmd.to_dict())

    def tune(self, cmd: TuneCommand) -> dict:
        plan = self.planner.tune(cmd)
        return self._commit(plan, kind="tune", payload=cmd.to_dict())

    def feedback_tick(self, measured_phase_deg: list[float]) -> dict:
        if self.last_plan is None:
            raise RuntimeError("no plan to correct")
        plan = self.loop.correct(self.last_plan, measured_phase_deg)
        return self._commit(plan, kind="feedback", payload={"measured": measured_phase_deg})

    def _commit(self, plan: Plan, kind: str, payload: dict) -> dict:
        self.fpga.push_plan(plan)
        self.hal.apply(plan)
        self.last_plan = plan
        packet = MeshPacket(node_id=self.cfg["node_id"], kind=kind, body={"command": payload, "plan": plan.to_dict()})
        return {"packet": json.loads(dumps(packet)), "plan": plan.to_dict(), "fpga": self.fpga.last_write}

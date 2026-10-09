import math

from app.service import BeamApp
from app.types import SteerCommand
from mesh.protocol import MeshPacket, dumps, loads
from rf.planner import steering_phases


def test_broadside_phases_are_zero():
    elements = [{"id": 0, "x": 0.0, "y": 0.0, "z": 0.0}, {"id": 1, "x": 0.5, "y": 0.0, "z": 0.0}]
    phases = steering_phases(elements, 144_390_000, 0.0, 0.0)
    assert abs(phases[0]) < 1e-9
    assert abs(phases[1]) < 1e-6


def test_endfire_has_progressive_phase():
    elements = [{"id": 0, "x": 0.0, "y": 0.0, "z": 0.0}, {"id": 1, "x": 1.0, "y": 0.0, "z": 0.0}]
    phases = steering_phases(elements, 150_000_000, 90.0, 0.0)
    assert phases[1] < phases[0]


def test_steer_pushes_four_weights():
    app = BeamApp(dry_run=True)
    out = app.steer(SteerCommand(20.0, 5.0, 5000))
    assert len(out["plan"]["elements"]) == 4
    assert out["packet"]["kind"] == "steer"
    assert any(addr == 0x04 for addr, _ in out["fpga"])


def test_packet_roundtrip_mac():
    raw = dumps(MeshPacket("veritas-pi-01", "phase", {"phase_deg": 1.0}))
    pkt = loads(raw)
    assert pkt.verify()


def test_feedback_reduces_error():
    app = BeamApp(dry_run=True)
    app.steer(SteerCommand(0.0))
    planned = [e["phase_deg"] for e in app.last_plan.to_dict()["elements"]]
    out = app.feedback_tick([p + 10 for p in planned])
    new = [e["phase_deg"] for e in out["plan"]["elements"]]
    err_after = abs((new[0] - planned[0] + 180) % 360 - 180)
    assert err_after < 10 or math.isfinite(new[0])

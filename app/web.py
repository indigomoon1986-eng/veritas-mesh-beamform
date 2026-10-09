"""python -m app.web"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from app.service import BeamApp
from app.types import SteerCommand, TuneCommand, load_config

app = FastAPI(title="Veritas Mesh Beamform")
beam = BeamApp(dry_run=True)


class SteerIn(BaseModel):
    azimuth_deg: float
    elevation_deg: float = 0.0
    freq_hz: float | None = None
    mode: str = "mrt"


class TuneIn(BaseModel):
    freq_hz: float
    amplitude: float = 0.5


class FeedbackIn(BaseModel):
    measured_phase_deg: list[float]


@app.get("/health")
def health():
    cfg = load_config()
    return {"node_id": cfg["node_id"], "array": cfg["array"]["name"], "ok": True}


@app.post("/steer")
def steer(body: SteerIn):
    return beam.steer(SteerCommand(body.azimuth_deg, body.elevation_deg, body.freq_hz, body.mode, "web"))


@app.post("/tune")
def tune(body: TuneIn):
    return beam.tune(TuneCommand(body.freq_hz, body.amplitude, "web"))


@app.post("/feedback")
def feedback(body: FeedbackIn):
    return beam.feedback_tick(body.measured_phase_deg)


def main() -> None:
    import uvicorn
    cfg = load_config()
    uvicorn.run(app, host=cfg.get("bind", "0.0.0.0"), port=int(cfg.get("web_port", 8787)))


if __name__ == "__main__":
    main()

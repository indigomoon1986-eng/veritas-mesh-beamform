"""CLI: python -m app.cli steer --azimuth 0 --elevation 10 --freq-hz 5000"""

from __future__ import annotations

import argparse
import json

from app.service import BeamApp
from app.types import SteerCommand, TuneCommand


def main() -> None:
    parser = argparse.ArgumentParser(prog="veritas-beam")
    sub = parser.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("steer")
    st.add_argument("--azimuth", type=float, required=True)
    st.add_argument("--elevation", type=float, default=0.0)
    st.add_argument("--freq-hz", type=float, default=None)
    st.add_argument("--mode", choices=["mrt", "zf"], default="mrt")
    tn = sub.add_parser("tune")
    tn.add_argument("--freq-hz", type=float, required=True)
    tn.add_argument("--amplitude", type=float, default=0.5)
    fb = sub.add_parser("feedback")
    fb.add_argument("--phase", type=float, nargs="+", required=True)
    fb.add_argument("--azimuth", type=float, default=0.0)
    args = parser.parse_args()
    app = BeamApp(dry_run=True)
    if args.cmd == "steer":
        out = app.steer(SteerCommand(args.azimuth, args.elevation, args.freq_hz, args.mode))
    elif args.cmd == "tune":
        out = app.tune(TuneCommand(args.freq_hz, args.amplitude))
    else:
        app.steer(SteerCommand(args.azimuth))
        out = app.feedback_tick(args.phase)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

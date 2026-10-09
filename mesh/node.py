"""python -m mesh.node"""

from app.types import load_config
from mesh.discovery import Discovery


def main() -> None:
    cfg = load_config()
    disc = Discovery(cfg["node_id"], int(cfg["mesh_port"]), cfg.get("bind", "0.0.0.0"))
    disc.open()
    print(f"veritas mesh beam discovery on :{cfg['mesh_port']} as {cfg['node_id']}")
    while True:
        disc.announce(0.0, cfg["array"]["frequency_hz"], 0.0)
        try:
            raw, addr = disc._sock.recvfrom(4096)
            peer = disc.ingest(raw, addr)
            if peer:
                print(f"peer {peer.node_id} phase={peer.phase_deg:.1f}")
        except TimeoutError:
            pass


if __name__ == "__main__":
    main()

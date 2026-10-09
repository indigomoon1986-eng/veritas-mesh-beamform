"""UDP discovery and phase gossip on the Veritas overlay."""

from __future__ import annotations

import socket
import time
from dataclasses import dataclass, field

from mesh.protocol import MeshPacket, dumps, loads


@dataclass
class Peer:
    node_id: str
    addr: tuple[str, int]
    last_seen: float
    phase_deg: float = 0.0
    freq_hz: float = 0.0
    azimuth_deg: float = 0.0


@dataclass
class Discovery:
    node_id: str
    port: int = 48750
    bind: str = "0.0.0.0"
    peers: dict[str, Peer] = field(default_factory=dict)
    _sock: socket.socket | None = None

    def open(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((self.bind, self.port))
        sock.settimeout(0.5)
        self._sock = sock
        return sock

    def announce(self, phase_deg: float, freq_hz: float, azimuth_deg: float):
        pkt = MeshPacket(self.node_id, "phase", {"phase_deg": phase_deg, "freq_hz": freq_hz, "azimuth_deg": azimuth_deg})
        if self._sock is not None:
            self._sock.sendto(dumps(pkt).encode(), ("255.255.255.255", self.port))
        return pkt

    def ingest(self, raw: bytes, addr: tuple[str, int]):
        try:
            pkt = loads(raw.decode())
        except (ValueError, UnicodeDecodeError):
            return None
        if not pkt.verify():
            return None
        peer = Peer(pkt.node_id, addr, time.time(), float(pkt.body.get("phase_deg", 0)), float(pkt.body.get("freq_hz", 0)), float(pkt.body.get("azimuth_deg", 0)))
        self.peers[pkt.node_id] = peer
        return peer

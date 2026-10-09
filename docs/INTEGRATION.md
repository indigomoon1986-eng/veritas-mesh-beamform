# Integration notes

Drop this tree at /opt/veritas-mesh-beamform on a node that already runs the Veritas image (batman-adv on wlan1, WireGuard on wg0).

1. Set node_id to the same id the pba-agent uses.
2. Point fpga.spi_device at the FPGA bridge. Dry-run until the bitstream is loaded.
3. Enable systemd/veritas-beamform.service.
4. Phase gossip uses UDP 48750 on the WireGuard subnet, not on the public AP.

Synthesize fpga/rtl/beamform_top for the part on the node. The host only writes weights and the frequency word.

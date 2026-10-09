# Veritas Mesh Beamform / SDR

Beamforming and software-defined radio layer for a Veritas Mesh node. It sits on the existing Raspberry Pi mesh (802.11s + B.A.T.M.A.N. + WireGuard) and adds a closed loop that steers a local phased array or coil bank through an FPGA.

This is an experimental communications stack for licensed amateur (Part 97) or ISM operation. It does not transmit by itself. Keep power, frequency, and identification inside the rules of the band you are actually on. Do not use it to jam, spoof, or interfere.

## Stack

app: steer / tune commands (CLI or web on the Pi)
mesh: node discovery, shared timing and phase, packet route
rf: phase offset, frequency, MIMO precoder weights
fpga: NCO carrier, digital phase, MIMO precoding, per-channel timing
hal: GPIO / SPI to varactors and relays on the LC tanks
feedback: FPGA telemetry back up through the mesh

Full tree is in the initial commit alongside this file.

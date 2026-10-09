# Veritas Mesh Beamform / SDR

Beamforming and software-defined radio layer for a Veritas Mesh node. It sits on the existing Raspberry Pi mesh (802.11s + B.A.T.M.A.N. + WireGuard) and adds a closed loop that steers a local phased array or coil bank through an FPGA.

Experimental communications stack for licensed amateur (Part 97) or ISM operation. It does not transmit by itself. Do not use it to jam, spoof, or interfere.

Sibling OTH path: https://github.com/indigomoon1986-eng/veritas-mesh-oth

## Stack

app: steer / tune commands (CLI or web on the Pi)
mesh: node discovery, shared timing and phase, packet route
rf: phase offset, frequency, MIMO precoder weights
fpga: NCO carrier, digital phase, MIMO precoding, per-channel timing
hal: GPIO / SPI to varactors and relays on the LC tanks
feedback: FPGA telemetry back up through the mesh

## Run

python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m app.cli steer --azimuth 0 --elevation 10 --freq-hz 5000
python -m app.cli tune --freq-hz 144390000
python -m app.web
python -m mesh.node
pytest -q

fpga/spi_bridge.py dry-runs when /dev/spidev0.0 is absent.

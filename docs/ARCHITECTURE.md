# Architecture

Veritas Mesh already forms the L2/L3 fabric. This repo is the RF plane.

Phase law: phi = -2 pi f (r dot u) / c. Azimuth 0 is broadside.

Register map: 0x00 control, 0x04 freq word, 0x10+8i real weight, 0x14+8i imag weight, 0x40 measured phase.

OTH sibling: veritas-mesh-oth. It reuses this register map and does not replace batman-adv.

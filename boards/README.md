# boards/ — per-device PCB projects

One directory per device variant (`boards/<device>/`): SKiDL sources, KiCad project,
BOM, and the device's integration descriptor (conforming to the bridge's pinned
device-integration convention — see `../contracts/README.md`). Ledger tasks touching a
board carry its `[dev:<board-slug>]` tag.

Empty at bootstrap: PCB work opens behind its governing DES design (`phase-gates`).

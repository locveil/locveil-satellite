# locveil-satellite

The ESP32 voice-satellite hardware product of the [Locveil](https://github.com/locveil)
family — room nodes that wake on a spoken name, stream audio to the
[locveil-voice](https://github.com/locveil/locveil-voice) backend, and play its spoken
replies, with smart-home actuation handled by
[locveil-bridge](https://github.com/locveil/locveil-bridge).

This repo owns everything device-side:

- **`boards/<device>/`** — PCB projects (SKiDL/KiCad), one per device variant.
- **`components/`** — shared ESP-IDF firmware components (`locveil_wifi`,
  `locveil_wb_mqtt`, `locveil_ota`, `locveil_identity`, `locveil_ir_baseband`); each
  device gets its own firmware app built from them.
- **`provisioning/`** — the WB7-side fleet-provisioning plane (nginx + home CA + operator
  scripts): device certificate bootstrap, mTLS-gated firmware/model serving, OTA.
- **`contracts/`** — version-pinned copies of the sibling-owned contracts this hardware
  conforms to (the voice WebSocket wire protocol, the voice wake-word pack, the bridge
  device-integration convention).
- **`docs/`** — the satellite design corpus and this repo's ledger/journal.

Status: bootstrap. The design corpus is in place; PCB and firmware work opens behind the
repo's design gates (see `docs/LEDGER.md`).

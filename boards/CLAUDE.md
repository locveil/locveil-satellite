# PCB phase — nested notes (`phase-gates`; wired by OPS-2)

One SKiDL/KiCad project per device: `boards/<device>/`; every task carries its
`[dev:<board-slug>]` tag (`per-device-tags`). **Gate: no PCB work before the governing DES
design is AGREED** (root CLAUDE.md `phase-gates`).

- **MCP set for PCB work:** `pcbparts` (part search across JLCPCB/Mouser/DigiKey,
  parametric filters, KiCad footprints, alternatives) + `serena` (semantic navigation of
  the SKiDL sources) + `espressif-docs` (module/strapping/electrical facts).
- **Before the first PCB session:** run `scripts/bootstrap_references.sh` — it clones SKiDL
  into gitignored `references/` for Serena; nothing is installed or built from it.
- **skidl-skills is NOT part of the toolchain** unless/until DES-2 adopts it
  (`no-execution-toolchain-at-bootstrap`).
- Every ESP32 pin assignment is checked against the strapping/bootstrap tables at design
  time — double-booked pins (the GPIO14 lesson) are a DES-review finding, not a bench
  surprise.
- Per-device descriptors (bridge convention, DES-4) live with the board project and must
  pass the CI conformance check against the `contracts/` schema pin.

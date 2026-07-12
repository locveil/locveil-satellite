# FW phase — nested notes (`phase-gates`; wired by OPS-2)

Shared ESP-IDF components live here (`locveil_wifi`, `locveil_wb_mqtt`, `locveil_ota`,
`locveil_identity`, `locveil_ir_baseband`); apps are **one per device** with compile-time
identity + an NVS identity assertion at boot (`per-device-apps` — the single-image FR-1
design is RETIRED; never reintroduce it). **Gate: NO firmware work of any kind before DES-3
is done** — DES-3 picks the execution layer (PlatformIO vs pioarduino-lineage vs native
`idf.py`) and includes the mandatory pin/strapping audit step (root CLAUDE.md
`phase-gates`).

- **MCP set for FW work:** `espressif-docs` (API/IDF facts — check the doc's IDF version
  against the project's, per DES-3's alignment decision) + `esp-component-registry`
  (existing components before writing new ones) + `serena` (semantic navigation).
- **No build/flash tooling is wired here yet** — the Espressif ESP-IDF *Tools* MCP
  (build/flash/monitor) is execution-side and joins only per DES-3's decision
  (`no-execution-toolchain-at-bootstrap`).
- `imports/bridge-esp32/src/` is frozen source material — mine it, never build it.
- Contracts are pins (`consumer-pins`): the voice WS doc wins over firmware convenience;
  the wake pack ships UNMODIFIED, hash-verified; rooms are provisioning-time NVS.
- A task that needs a bench carries `HW-GATED` and never blocks a software milestone.

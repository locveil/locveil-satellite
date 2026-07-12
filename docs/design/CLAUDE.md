# DES phase — nested notes (`phase-gates`; wired by OPS-2)

Design docs live here. DES is the FIRST gate: no PCB task before its governing design is
AGREED; no FW task of any kind before **DES-3** is done (root CLAUDE.md `phase-gates`).

- **MCP set for DES work:** `espressif-docs` (fact-check chip/IDF claims against official
  docs — never from memory) + `esp-component-registry` (what exists as a maintained
  component before designing it). `pcbparts` joins when a design touches part selection.
- **Corpus ground rules (DES-1):** `imports/bridge-esp32/docs/wb-*.md` are bench-confirmed
  **leaf truth** — a newer, more general doc never downgrades a bench-CONFIRMED fact to
  VERIFY; merge claim-by-claim. Pin maps get re-audited against the datasheet/TRM strapping
  tables (the GPIO14 lesson).
- **Consumed contracts are read-only:** `contracts/` pins win over local assumptions; the
  voice WS doc is the wire-protocol source of truth (`consumer-pins`).
- No toolchain installs from a design session — PlatformIO is DES-3's decision,
  skidl-skills is DES-2's (`no-execution-toolchain-at-bootstrap`).

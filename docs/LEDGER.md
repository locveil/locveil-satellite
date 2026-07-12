# locveil-satellite — active ledger

Single source of scope + status (shared discipline: the `shared-invariants` block in
CLAUDE.md; mechanics: `../locveil-commons/process/ledger-discipline.md`). Completed
entries MOVE to `LEDGER_DONE.md` in the same change as their journal entry.

Born backlog seeded at bootstrap from board **PROD-15** (council HK-4, 2026-07-12); the
board lists these as seed only and never asserts their status — this ledger owns it.
Phase order is LAW: **DES → PCB → FW** (`phase-gates` invariant); no FW task starts
before **DES-3** is done.

## Design & review index

| Document | Backs |
|---|---|
| _(populated as the migrated corpus lands and DES docs are written)_ | |

## DES — design

- [ ] **DES-1** [fleet] — **Harmonize the bridge ESP32 doc corpus claim-by-claim.** The
      bridge's fresh general ESP32 doc is newer but WEAKER than its bench-confirmed build
      docs (HK-4 round 1: it downgrades bench-CONFIRMED facts to VERIFY) — merge
      claim-by-claim, never newest-wins; build docs are leaf truth. Includes the
      REQUIREMENTS truth pass and the pin-map re-audit (the GPIO14 double-booking lesson).
      Input corpus arrives with the bridge's export task (PROD-15 bridge delegation item 1).
- [ ] **DES-2** [fleet] — **skidl-skills review / rethink / adoption** (focused session,
      HK-4 round 4). Deliberately NOT installed at bootstrap
      (`no-execution-toolchain-at-bootstrap`); this task decides whether/how it enters the
      PCB toolchain alongside Serena-over-cloned-SKiDL.
- [ ] **DES-3** [fleet] — **Firmware execution-layer decision** — PlatformIO vs
      pioarduino-lineage vs native `idf.py`, including docs-MCP ↔ IDF-version alignment,
      the background-monitor pattern, and a **mandatory pin/strapping audit step**.
      **MANDATORY before any FW phase starts** (`phase-gates`). The
      PIO-platform-vs-latest-IDF tension is a fact-check, not a blind bet (HK-4 round 4).
- [ ] **DES-4** [dev:deck] — **Adopt the bridge's device-descriptor format for the deck
      devices.** Consumes the bridge's device-integration-convention design (PROD-15 bridge
      delegation item 2; "convention down, descriptors up") — author the conforming
      per-device descriptors (required timing/availability fields, `confirm_latency_ms`
      STATIC), mirror the pin under `contracts/`, wire the CI conformance check.

## PCB — board projects

_(none yet — opens after the governing DES designs; one `boards/<device>/` project per
device, tasks tagged `[dev:<board-slug>]`)_

## FW — firmware

_(gated on DES-3 — `phase-gates`)_

## OPS — operations / toolchain

- [ ] **OPS-1** — **Own the firmware/model publish pipeline into the WB7 `/srv/esp32/`.**
      The Plane-B nginx serves `/esp32/firmware/` + `/esp32/models/` from
      `/srv/esp32/{firmware,models}/` (operator-managed static); this repo owns how
      artifacts get published there (versioning, hashes, the wake-pack pin flow).
- [ ] **OPS-2** — **Wire the day-one toolchain** (HK-4 round 4): pcbparts MCP + Espressif
      docs MCP + component-registry MCPs; Serena over gitignored `references/` clones
      (SKiDL) + a bootstrap script; a single root `.mcp.json`. Also wires the per-phase
      nested CLAUDE.md + MCP sets (`phase-gates`). Knowledge-side only — no PlatformIO, no
      skidl-skills (those are DES-3 / DES-2 decisions).

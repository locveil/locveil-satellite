# locveil-satellite — agent notes

The ESP32 voice-satellite product repo — the hardware member of the Locveil family (siblings
on disk: `../locveil-voice` the voice backend, `../locveil-bridge` the device bridge,
`../locveil-commons` the umbrella). It owns the satellite PCB projects (SKiDL/KiCad under
`boards/<device>/`), the ESP-IDF firmware (shared `components/` + per-device apps),
enclosures, the WB7-side fleet-provisioning plane (`provisioning/` — nginx Plane B), and the
`contracts/` pins of sibling-owned artifacts. Born from council HK-4 → board PROD-15
(2026-07-12), instantiated from `../locveil-commons/process/new-repo-template/`; the design
corpus migrated from `../locveil-voice` (see `docs/JOURNAL.md`).

## Invariants (repo-local LAW — owned here, never inside shared blocks)

- **`esp32-only-charter`** — scope is the ESP32 voice satellite (HK-4). It escalates to
  embedded-generally ONLY if the HVAC ESP8266 firmware rewrite ever happens (the recorded
  trigger); HVAC drivers/configs stay bridge-side ALWAYS.
- **`phase-gates`** — normative task order **DES → PCB → FW** with per-phase nested
  CLAUDE.md + MCP sets (wired by OPS-2). No PCB work before its governing DES design is
  AGREED; **no FW work of any kind before DES-3 is done** (the execution-layer decision,
  including the mandatory pin/strapping audit step — the GPIO14 lesson). A task names the
  phase it belongs to via its prefix.
- **`hw-gated`** — a task that cannot complete without physical hardware carries the
  **`HW-GATED`** marker; it never blocks a software milestone and is picked up only when the
  bench is available.
- **`per-device-tags`** — every PCB/FW task carries its device tag (`[dev:<board-slug>]`,
  one per `boards/<device>/` project); genuinely device-independent work is tagged
  `[fleet]`. DES/OPS tasks tag only when device-specific.
- **`per-device-apps`** — firmware = shared ESP-IDF components (`locveil_wifi`,
  `locveil_wb_mqtt`, `locveil_ota`, `locveil_identity`, `locveil_ir_baseband`) + **one app
  per device** with compile-time identity + an NVS identity assertion at boot. The FR-1
  single-image design is RETIRED (HK-4 round 3 — the GPIO14 double-booking); never
  reintroduce a multi-device image. Rooms are provisioning-time NVS, the voice registry is
  authoritative (an optional build-time NVS default seed is allowed).
- **`consumer-pins`** — this repo CONSUMES three versioned sibling artifacts, pinned one-way
  inward under `contracts/` (never hand-edit a pin; re-pin on a vN bump — see
  `contracts/README.md`):
  - **voice WS wire protocol** — `../locveil-voice/docs/guides/websocket-api.md` is the
    single source of truth (voice's `ws-protocol-doc-canonical`); the doc wins, firmware
    adapts.
  - **voice wake-word pack** — flash-time pin of voice's UNMODIFIED artifact
    (hash-verifiable; pack version reported in `register`; OTA model updates optional/later).
    Never retrain or modify the pack here.
  - **bridge device-integration-convention** — "convention down, descriptors up": the bridge
    owns the versioned convention; this repo owns the conforming **per-device descriptors**
    (required timing/availability fields; `confirm_latency_ms` is STATIC). Fully DESIGN-TIME
    — vocabulary reconciliation happens at the DES gate, no runtime negotiation; the one
    retained firmware-version topic is the stale-pin tripwire.
- **`no-execution-toolchain-at-bootstrap`** — no PlatformIO install and no skidl-skills
  install until DES-3 / DES-2 decide them (HK-4 round 4, owner amendment). Day-one toolchain
  is knowledge-side only: pcbparts MCP + Serena-over-cloned-SKiDL (PCB), Espressif docs +
  component-registry MCPs (FW) — wired by OPS-2.

## Ledger & journal

Active ledger `docs/LEDGER.md` · DONE `docs/LEDGER_DONE.md` · journal `docs/JOURNAL.md`
(newest on top). Prefixes: `DES` (design), `PCB` (board projects), `FW` (firmware), `OPS`
(operations/toolchain). Everything else — the triad, rotation, watermarks — is the shared
discipline below; mechanics live in `../locveil-commons/process/ledger-discipline.md`.

## Shared blocks (pinned — `process/claude-md.md`; edit in commons, then re-pin)

<!-- locveil:begin shared-invariants scope-v5 -->
**Locveil shared process invariants** — digest; normative source: `../locveil-commons/process/`
(`ledger-discipline.md`, `claude-md.md`, `user-docs.md`). On disagreement the process files
win. Never edit this block in place — edit in commons, then re-pin (`process/claude-md.md` §3).

- **ledger triad** — active ledger + DONE ledger + one rotating journal; completion MOVES
  the entry to DONE and journals it in the same change; rotation only via an explicit
  `scope_guard.py --rotate` in its own commit; watermarks + mechanics:
  `process/ledger-discipline.md`.
- **every-task-in-the-ledger** — no work without a ledger ID; a doc finding becomes scope
  only when a ledger task declares it.
- **task-start-reconciliation** — before executing any task, verify its claims against repo
  reality; narrow or redefine at intake rather than executing stale text.
- **design-then-implement** — non-trivial changes get a reviewed design doc before code.
- **review-then-remediate** — review findings become ledger tasks before they get fixed.
- **user-facing-docs-are-done** — every completion entry records a docs verdict
  (`docs: <node-ids>` or `docs: none — <why>`) against the repo's `docs/manifest.json`;
  caused staleness is fixed in the same change, discovered staleness is filed against the
  next release gate; scope + manifest schema + style: `process/user-docs.md`.
- **Enforcement** — vendored `scope_guard.py` at a pinned `scope-vX` tag + committed
  pre-commit hook + path-gated `ledger-guard` CI job; hooks and CI run `--check` only.
<!-- locveil:end shared-invariants -->

<!-- locveil:begin cross-repo-board scope-v4 -->
**Locveil cross-repo: the board.** The repos are SIBLINGS on disk — `../locveil-commons`
(umbrella: board, `process/`, shared packages), `../locveil-voice`, `../locveil-bridge`,
`../locveil-satellite`.
Cross-repo initiatives live at `../locveil-commons/board/BOARD.md` (`PROD-N`; council
topics `HK-N`; completed entries in `BOARD_DONE.md`). Delegations arrive as board-as-outbox
text committed inside a PROD entry: pull it, verify per `task-start-reconciliation`, file
it under a LOCAL task ID, execute locally, then write that ID back into the board entry.
The board never asserts a delegated task's status — this repo's ledger owns it. Direct
operational filings between product repos (bug reports, contract requests) stay
repo-to-repo and don't need the board. Cross-repo design sessions and the council run FROM
locveil-commons (convention: `../locveil-commons/process/council.md`); decisions land on
the board, never in chat.
<!-- locveil:end cross-repo-board -->

# locveil-satellite — journal (newest on top)

Dated record of work done; rotates per `ledger-discipline.md` §2 (whole days into
`docs/archive/journal/`, pointer here).

## 2026-07-12 — cross-repo-board block re-pinned @ scope-v4 (PROD-15 close follow-through)

The shared block now names this repo (`../locveil-satellite`) as the fourth sibling; block
text between the markers + the `.scope-guard.toml` hash updated from the commons source per
the `process/claude-md.md` §3 flow (mechanical re-pin, no other content change —
journal-line only, no ledger task). PROD-15 closed on the board the same day.

## 2026-07-12 — deck corpus harmonized, docs/devices/ layer born (DES-1)

Interactive session. Owner decisions: three-layer doc taxonomy (architecture/ =
narratives, design/ = decisions, **devices/ = per-device hardware ground truth** — the
voice satellite gets its own dossier there at PCB phase); slugs **revox-a77 / revox-b215
/ pioneer-cld925 / panasonic-fs90** (fix the `[dev:]` tags + future `boards/<slug>/`);
trim to engineering truth; imports deleted in this close. Landed: `docs/devices/`
(deck-common + 4 dossiers + img/), `docs/review/des1-truth-pass.md`. Merge headline:
build docs won 7/8 direct conflicts (B215 "RS-232 vs TTL" dissolved — it's open-collector
Serie I/O; A77 "switch common" model was wrong — pin PAIRS), but the FS90
**rail-isolation check went the other way** — the newer build doc had dropped the
research pass's non-negotiable safety gate; reinstated. Code sweep: zero unique bench
truth (placeholders throughout); GPIO14 triple-booked across three drivers — the
concrete `per-device-apps` evidence, now recorded in deck-common §5. Pin re-audit vs
Espressif docs: no legacy pin sits on a strapping pin; GPIO14=MTMS noted.
`imports/bridge-esp32/` deleted (absorbed; import commit `0d950a9` keeps it resolvable);
bridge VWB-38 note filed repo-to-repo (wb-mqtt-v1 promotion source → the truth pass §2).
Owner verdict on the imported code recorded: reference-only, docs were the value.

## 2026-07-12 — day-one toolchain wired (OPS-2)

Root `.mcp.json` (the single MCP config, per HK-4 round 4): `pcbparts` + `espressif-docs`
+ `esp-component-registry` (all HTTP; docs server needs a one-time GitHub OAuth via `/mcp`
— a 401 before that is expected, and it's rate-limited 40/h · 200/day per user) + `serena`
(stdio via `uvx`, project-from-cwd). `scripts/bootstrap_references.sh` clones SKiDL into
gitignored `references/` for Serena — run today, clone verified, gitignore holds; pcbparts
and the registry answered 200 to an MCP initialize probe. Per-phase nested CLAUDE.md
landed: `docs/design/` (DES), `boards/` (PCB), `components/` (FW) — each states its
`phase-gates` gate + MCP set. Deliberately absent (`no-execution-toolchain-at-bootstrap`):
PlatformIO (DES-3), skidl-skills (DES-2), and the ESP-IDF *Tools* MCP (build/flash —
execution-side, rides DES-3; noted in `components/CLAUDE.md` so nobody wires it early).

## 2026-07-12 — bridge ESP32/ tree imported (DES-6; PROD-15 bridge delegation item 1b)

Board-intake reconciliation found the one delegated action without a local ID: the bridge's
frozen `ESP32/` deck-bridge scaffold awaited a satellite-side pull (bridge DRV-35 BLOCKED on
our confirmation). Filed **DES-6**, executed same session: 34 git-tracked files @ bridge
`a80322f` → `imports/bridge-esp32/`, verbatim (rules + provenance: `imports/README.md`).
Value is the *facts*, not the architecture — the bench-confirmed `docs/wb-*.md` build docs
are DES-1's leaf truth, `REQUIREMENTS.md` feeds its truth pass (and bridge VWB-38's
wb-mqtt-v1 promotion), `src/` is FW-phase component material; the single-image FR-1 shape
stays retired (`per-device-apps`). Confirmation written into bridge DRV-35 (repo-to-repo
filing) so its delete + DRV-7 retirement can proceed.

## 2026-07-12 — design corpus + provisioning plane imported from locveil-voice (BUILD-22)

Plain moves, frozen history stays in voice (`git -C ../locveil-voice log --follow` for
pre-move history). Landed: `docs/design/esp32_satellite.md` (the authoritative ARCH-22
consolidated design; §4.1–4.3 wire tables demoted to a pointer at voice's
`websocket-api.md` + the `contracts/` pin, per the PROD-15 delegation),
`docs/design/ws_esp32_transport.md` (superseded lineage, frozen),
`docs/architecture/esp32.md` + `docs/images/esp32-{fit,turn}.{dot,png}` (cross-repo links
re-pointed), and the **Plane-B fleet-provisioning tree** voice `nginx/` → `provisioning/`
(D-6-as-amended; ansible playbook + CA/provisioning scripts + nginx site template; the
operator-local `inventory.ini`/`group_vars/all.yml` copied on disk and gitignored here —
the WB7 deployment itself is untouched, this is a repo-side handover). Voice keeps a
pinned copy of `esp32-site.conf.j2` for its TLS-e2e test (its tether; re-pin direction is
voice-pulls-from-here). Imported tasks: **DES-5** (ex voice ARCH-44, cert lifecycle) +
**FW-1** (ex voice ARCH-23, firmware build — reconcile at start, HK-4 amendments noted
inline). Interim WS-protocol pin recorded in `contracts/README.md`.

## 2026-07-12 — repo bootstrapped from process/new-repo-template

Instantiated by voice **BUILD-22** (board **PROD-15**, council HK-4) from
`../locveil-commons/process/new-repo-template/` at **scope-v3** — CLAUDE.md with the two
pinned shared blocks + the repo-local LAW (esp32-only-charter, phase-gates, hw-gated,
per-device-tags, per-device-apps, consumer-pins, no-execution-toolchain-at-bootstrap),
ledger triad, vendored `scripts/scope_guard.py` @ scope-v3, pre-commit hook
(`core.hooksPath hooks`), `ledger-guard` CI. Skeleton directories: `components/`,
`boards/`, `provisioning/`, `contracts/`. Born backlog DES-1..DES-4 + OPS-1..OPS-2 seeded
from the PROD-15 entry. No deviations from the template.

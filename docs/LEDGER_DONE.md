# locveil-satellite — DONE ledger

Completed entries, MOVED here on close. Frozen history — never re-edited. Rotates per
`ledger-discipline.md` §2 (archived IDs stay resolvable via `docs/archive/ledger/`).

## DES — design

- [x] **DES-1** [fleet] — **DONE 2026-07-12** — **Harmonize the bridge ESP32 doc corpus
      claim-by-claim** (interactive session, owner decisions inline). Output: the new
      `docs/devices/` layer (owner-decided three-layer taxonomy) — `deck-common.md` +
      four dossiers, slugs fixed as `revox-a77` / `revox-b215` / `pioneer-cld925` /
      `panasonic-fs90`; manual scans → `docs/devices/img/`. Evidence:
      `docs/review/des1-truth-pass.md` — 10 conflict resolutions (build docs won 7/8
      direct conflicts; the FS90 rail-isolation check went the OTHER way — the newer doc
      had dropped a safety requirement, reinstated as that dossier's gating bench item),
      full REQUIREMENTS FR/NFR/C/EI disposition (the VWB-38 wb-mqtt-v1 promotion feed),
      code sweep (no unique bench truth; GPIO14 triple-booking recorded — the
      `per-device-apps` lesson), ESP32 pin re-audit vs official Espressif docs (no legacy
      pin on a strapping pin; GPIO14=MTMS note). `imports/bridge-esp32/` deleted in this
      close (absorbed; resolvable at `0d950a9`); repo-to-repo note filed to bridge VWB-38
      re-pointing the promotion source at the truth pass.

- [x] **DES-6** [fleet] — **DONE 2026-07-12** (filed + executed same session; PROD-15 bridge
      delegation item 1b, satellite side). **Import the frozen bridge `ESP32/` tree.** The 34
      git-tracked files copied 1:1 from `../locveil-bridge/ESP32/` @ bridge `a80322f` into
      `imports/bridge-esp32/` (frozen reference — provenance + mining rules in
      `imports/README.md`; untracked local files and `.pio/` build output left behind; no
      history migration per the plain-move rule). This is DES-1's input corpus (bench-confirmed
      `docs/wb-*.md` build docs = leaf truth, `REQUIREMENTS.md` for the truth pass) and FW-phase
      source material (`src/`+`include/` → shared `components/`, per HK-4 the single-image
      architecture itself stays retired). Import confirmation filed repo-to-repo into the
      bridge's DRV-35 entry — unblocks its delete + DRV-7 retirement.

## PCB — board projects

## FW — firmware

## OPS — operations / toolchain

- [x] **OPS-2** — **DONE 2026-07-12** — **Wire the day-one toolchain** (HK-4 round 4;
      knowledge-side only per `no-execution-toolchain-at-bootstrap`). Root `.mcp.json` with
      the four servers: `pcbparts` (HTTP `https://pcbparts.dev/mcp`, keyless — JLCPCB/
      Mouser/DigiKey parametric search + KiCad footprints), `espressif-docs` (HTTP
      `https://mcp.espressif.com/docs` — OAuth via GitHub on first `/mcp` use; 401 until
      then is expected; 40 req/h / 200 req/day per user), `esp-component-registry` (HTTP
      `https://components.espressif.com/mcp`, keyless), `serena` (stdio, `uvx` from
      `oraios/serena`, `--project-from-cwd`). `scripts/bootstrap_references.sh` clones SKiDL
      into gitignored `references/` for Serena (run + verified: clone lands, gitignore
      holds; pcbparts + registry probed 200 on MCP initialize). Per-phase nested CLAUDE.md
      wired: `docs/design/` (DES — docs+registry MCPs, corpus ground rules), `boards/` (PCB
      — pcbparts+serena, bootstrap prereq, strapping-audit rule), `components/` (FW —
      DES-3 gate, docs+registry, Tools-MCP explicitly deferred to DES-3). No PlatformIO, no
      skidl-skills, no ESP-IDF Tools MCP — DES-3/DES-2 own those decisions.

- [x] **OPS-3** [fleet] — **DONE 2026-07-12** (filed + executed same session; PROD-16
      satellite delegation item 1; convention: `../locveil-commons/process/contracts.md`).
      **Contracts pins-shape restructure + contract-guard adoption.** Landed: `contracts/`
      in the uniform org shape with the registry README (replacing the bootstrap table —
      reconciliation found ALL THREE rows stale the same day, not the one line the
      delegation named). Pins, strict-conformant from day one (full `files` sha256 maps):
      `pins/ws-protocol/` upgraded from the interim commit-ref pin (voice `98e8fd0`) to a
      COMPLETE stamped artifact-copy pin @ **`ws-protocol-v1`** — the delegation's
      "PIN.json now, stamped pin when the tag lands" collapsed to one step because voice
      ARCH-47 had ALREADY tagged (voice `9f371b9`; the doc moved +17/−3 in between, so
      re-pinned at the tag); `pins/wake-pack/` first stamped pin @ **`wake-pack-v1`**
      (sidecar STAMP with HF sha256s; pack binaries never enter the tree). NEW owned
      surface found at reconciliation: voice already consumes this repo's Plane-B nginx
      template as a pre-tag pin "waiting for the owner stamp" — stood up
      `contracts/esp32-site/` (STAMP + pointer README), tagged **`esp32-site-v1`**
      (byte-identical to voice's pinned copy @ `37dcac5`), day-one owner guard
      `scripts/check_esp32_site.py` (9 guaranteed-surface markers; template comment-path
      nit recorded, deferred to the next real bump — any byte change is a version bump).
      Enforcement wired: vendored `scripts/contract_guard.py` @ **`contract-guard-v1`**,
      `contract-guard` CI job (path-gated, `--check` only), pre-commit chain
      (scope-guard → contract-guard → esp32-site guard). Both guards green, 0 warnings.
      Conformance pointers are honest forwards (no test infra pre-FW): ws-protocol → FW-1,
      wake-pack → OPS-1 hash-at-publish + FW-1 hash-at-flash. Same change: DES-4 amended
      (pins-shape mirror + the bridge tag/STAMP wrinkle at intake), OPS-1 amended
      (hash-at-publish), board write-back into PROD-16.

- [x] **OPS-4** [fleet] — **DONE 2026-07-12** (filed + executed same session; PROD-17
      satellite delegation, all three items under one ID; convention:
      `../locveil-commons/process/user-docs.md` + `process/user-docs/manifest.schema.json`).
      **User-docs convention adoption: manifest + CONTRIBUTING + provisioning pass +
      scope-v5.** Landed: (1) `docs/manifest.json` (7 nodes; surfaces provisioning/
      contracts/devices/boards/firmware) + `contracts/docs-manifest/` STAMP
      `docs-manifest-v1` (INTERNAL registry row; no git tag — bumps only on schema
      reshape) + coherence guard `scripts/check_docs_manifest.py` (schema-vocabulary,
      node↔tree, roots sweep, floor, derives_from, canonical targets; wired into
      pre-commit as the 4th stage + the `contract-guard` CI job). Floor staffed 5/5
      where capability exists: front-door (README, banner-honest), operator
      (provisioning runbook), contributor (NEW `CONTRIBUTING.md` — phase process, pin
      discipline, leaf-truth corpus rule, per-phase toolchain map),
      canonical-reference (the `esp32-site` owned surface — stamp + guard from OPS-3),
      quickstart as a declared pending-gate; FW-gated docs are pending-gate nodes
      naming gates (`FW-1 first light`; deck build docs gate on first bench-verified
      board, `derives_from` the four `docs/devices/` dossiers); no end-user class
      (no report pipeline here — capability carve-out). (2) Provisioning-README
      user-grade pass: reader-first opener; tracking refs stripped (ARCH/D/PROD IDs,
      design-doc paths); the `.pio` publish line replaced with an
      execution-layer-neutral note (toolchain finalizes with DES-3 — recorded in the
      manifest node, not the doc); DISCOVERED-and-fixed in the same section: the stale
      `jarvis.*` pack example → `irina.*`, and the publish flow now tells the operator
      to verify pack sha256s against the pinned wake-pack stamp (the OPS-1 amendment's
      doc face). (3) scope-guard re-pinned `scope-v3`→`scope-v5` (1.2.0):
      shared-invariants block re-pinned (gains `user-facing-docs-are-done`), toml hash
      updated, `docs_verdict_since = 2026-07-13` (day AFTER the re-pin: the four
      2026-07-12 completions predate the rule; DONE is frozen history). Also: root
      README ledger-pointer stripped + doc index added. All four guards green.
      Reconciliation nit filed upstream in the write-back: the commons skeleton
      manifest's `$comment` key violates the schema's own `additionalProperties: false`.
      docs: readme, contributing, provisioning-runbook
- [x] **OPS-5** [fleet] — **DONE 2026-07-14** (board delegation **PROD-22**, executed by the
      commons session on owner instruction; note: PROD-22's original delegation list named
      bridge+voice only — satellite added at execution for completeness, it vendors the same
      guard). **Re-vendor contract-guard @ `contract-guard-v2`** (1.1.0, the `TAG-MISSING`
      rule). The rule fired here too — third instance of the false-green class:
      `contracts/docs-manifest/STAMP.json` named `docs-manifest-v1` with no tag behind it;
      tag created at the STAMP's landing commit, check green 0 warnings. docs: none —
      vendored tool only.

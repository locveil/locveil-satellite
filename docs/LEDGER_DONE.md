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
- [x] **OPS-7** [fleet] — **DONE 2026-07-14** (sprint-01 selected row — named "OPS-1a"
      there, renumbered at intake: scope-guard IDs are numeric-only; split from OPS-1
      at intake the same day). **Model-pack publish flow — hash-at-publish vs the
      wake-pack STAMP.** Landed `scripts/publish_model_pack.py` (stdlib-only,
      workstation-side — the STAMP is repo truth and lives here; transport is plain
      ssh/scp; NOT privileged — no CA key, stays outside the DES-5 broker by design):
      `verify` and `publish --node <client_id>... (--dest DIR | --host)` — sources
      fetched from the STAMP's own URLs or taken via `--from`; every file's sha256
      MUST match `contracts/pins/wake-pack/STAMP.json` before anything lands in
      `/srv/esp32/models/<client_id>/` (PROD-16 amendment, `process/contracts.md` §4
      binary-pack class), remote copies re-hashed post-copy. Execution-time decisions:
      per-node dirs get identical fleet-pack copies (per-node divergence is a future
      pin concern); a published file differing from the STAMP is REFUSED (per the
      STAMP's own note, replacing a published model is a breaking change — flashed
      hashes stop verifying), override is explicit `--allow-replace` after a pin bump;
      re-runs idempotent; client_id validated `^[A-Za-z0-9_-]+$` (the CSR scripts'
      untrusted-input rule). Verified end-to-end against the live upstream (HF fetch,
      both hashes green) + the full local matrix (publish, idempotent skip, drift
      refusal, allow-replace, tampered-source abort with nothing published,
      path-traversal id rejected); the ssh branch mirrors the local one and awaits a
      controller session — flagged, not asserted. README publish section rewritten
      around the tool (firmware half stays plain copies — OPS-1, dormant).
      docs: provisioning-runbook
- [x] **OPS-8** [fleet] — **DONE 2026-07-15** (board delegation **PROD-25**, filed off
      bridge OPS-30's finding). **CI checkout fetches tags for contract-guard.**
      contract-guard-v2's `TAG-MISSING` rule resolves owned STAMP tags via `git tag -l`,
      but the default `actions/checkout` clone is shallow AND tag-less — the guard job
      could never pass once v2 landed. Fix per `process/contracts.md` §4 (PROD-25
      amendment): `fetch-tags: true` on the guard job's checkout (shallow stays fine —
      the rule only needs the tag ref). Reconciliation vs the board text: PROD-25's sweep
      recorded satellite "vendored at v1, fix rides the v2 re-pin" — stale; OPS-5 had
      already re-vendored v2 on 2026-07-14, so this repo's job was latently broken NOW
      (both owned STAMPs name tags: `esp32-site-v1`, `docs-manifest-v1`) and the fix
      lands standalone. Verified by reproduction: tag-less shallow clone → 2× false
      TAG-MISSING, exit 1; after `git fetch --tags --depth 1` → green, 0 warnings. Also
      fixed in the same touched file: the workflow header comment still said
      "@ contract-guard-v1" (staleness caused by OPS-5's re-vendor). docs: none — CI
      workflow internals, no user-facing surface.
- [x] **OPS-9** [fleet] — **DONE 2026-07-15** (post-completion defect in OPS-8, caught
      by watching the pushed run — CI run 29414821199 FAILED with the same 2×
      TAG-MISSING). **The convention's `fetch-tags: true` one-liner does not work**:
      actions/checkout#1467 — on the default shallow single-commit fetch the flag only
      drops `--no-tags`, and git tag auto-following can't see tags on unfetched commits,
      so tags pointing at older commits never arrive (the checkout log shows the fetch
      command carries no tag refspec). OPS-8's local repro passed because
      `clone --no-tags` + `fetch --tags` is not checkout's actual fetch shape — repro
      fidelity lesson recorded. Fix: explicit `git fetch --tags --depth=1 origin` step
      after checkout (replaces the dead flag); re-verified from checkout's EXACT clone
      state (init + single-sha depth-1 fetch → guard fails; explicit tag fetch → green,
      0 warnings); this commit's own pushed run is the live confirmation, monitored to
      completion with the verdict recorded in the board write-back (not pre-asserted
      here — the OPS-8 lesson). Cross-repo blast radius written back to
      PROD-25: commons' own post-fix run dd7c270 FAILED the same way (its "EXECUTED"
      deliverable (2) is defective, convention §4 amendment (1) prescribes the dead
      one-liner); voice BUILD-38 verified "by simulation" — likely same latent state.
      docs: none — CI workflow internals, no user-facing surface.

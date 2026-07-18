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

- [x] **DES-3** [fleet] — **DONE 2026-07-17** — **Firmware execution-layer decision**
      (interactive owner session; decision doc **`docs/design/fw_execution_layer.md`**,
      AGREED — the `phase-gates` FW gate LIFTS). Decisions: **E-1 native `idf.py`, NO
      PlatformIO** (D-3 amended; evidence: the 2024 split froze Arduino-only — official
      PIO does espidf at 6.0.1 but has no 6.0.2, structurally trails, and is outside
      Espressif's supported v6 tooling; pioarduino espidf = 5.5.4/Arduino-centric;
      per-device-apps maps 1:1 onto plain IDF projects + shared `components/`).
      **E-2 IDF v6.0.2, spike-gated**: module research found exactly ONE v6-blocked
      dependency — `esp-tflite-micro` 1.3.7 (CI ≤5.5; maintainer-confirmed issue #125
      "use v5.5 for now", v6 promised) — so the FW phase's first act is a compat spike
      building its core on 6.0.2; pass → pin + report upstream, fail → port and
      CONTRIBUTE (owner-sanctioned), bail-out v5.5.4 (existing v5.5.0 tree the base).
      **E-3 dependency matrix** (registry, verified): esp_lcd_spd2010 2.0.0 explicitly
      v6-compatible; esp_websocket_client 1.7.0 (IDF6 CI, mTLS), mdns 1.11.3,
      esp_io_expander_tca9554 2.0.3 (new i2c_master API), esp_lvgl_port 2.8.0 (IDF6
      fixes; LVGL pinned ^9), cJSON now a registry dep; v6 notes: warnings-as-errors
      (vendored µVAD source), mbedTLS-4/PSA (~+40 KB; D-17 CSR-gen = FW-1 check item).
      **E-4 REST API on core `esp_http_server`** + D-16 amendment: Stage 2 REST-only
      (workbench page is the UI), Stage-1 SoftAP portal stays (mitsubishi2wb pattern;
      its form may slip past v1 — build-time NVS seed covers the on-desk units).
      **E-5** background-monitor pattern defined (idf.py steps as background Bash
      tasks). **E-6** mandatory pin/strapping audit step defined (dossier + datasheet
      tables before first flash; already discharged for `waveshare-lcd146`).
      Toolchain install split out as **INFRA-1** (owner: new `INFRA` category; prefix
      registered in CLAUDE.md + `.scope-guard.toml` this change). docs: none — design
      artifact + ledger; user-facing guides remain pending-gate on FW-1 first light.

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

- [x] **DES-7** — **DONE 2026-07-17** — **Voice-satellite hardware adoption: Waveshare
      ESP32-S3-Touch-LCD-1.46B** (owner decision 2026-07-16 — off-the-shelf, 3 units on
      hand, no custom PCB; executed as an interactive owner session). Slug fixed at
      execution (owner): **`waveshare-lcd146`**. Landed:
      **(a)** dossier **`docs/devices/waveshare-lcd146.md`** — full pin/strapping map
      (official schematic p.1 GPIO matrix + vendor demo @ `fda89ff` + wiki, cross-checked
      claim-by-claim, per-file/line cites), strapping audit vs the ESP32-S3 datasheet/TRM
      (notable: straps **GPIO45/46 double as LCD QSPI DATA1/DATA0** — vendor-designed-in,
      safe at reset via the chip's weak pull-downs, download-mode caution recorded as a
      bench item; the GPIO14-lesson pass is otherwise clean), audio wiring truths
      (32-bit/RIGHT-slot mic capture; NO amp-enable GPIO — NS8002 hardwired on, trimmer
      volume; disjoint mic/DAC pin sets → the S3's two I2S peripherals carry D-8's two
      rates), TCA9554-gated LCD/touch resets (bring-up landmine), the vendor's stale
      `SD D3=21` define flagged, present-but-unused inventory, `HW-GATED` bench items.
      **(b)** `esp32_satellite.md` decision-log amendments: **D-2** (board adopted;
      display support an OPTIONAL compile-time feature, headless baseline; variant-B
      waveform listening-animation spec folded in; touch present-but-unused — scope
      decided at FW-1 intake, not DES-3); **D-7/D-8** (PCM5101A+NS8002 as the MAX98357A
      functional substitute; NO AEC path — §14's v2 audio-hardware upgrades CLOSED, v2 =
      new hardware); **D-9/D-12** (µVAD compiled into the app image, vendored source with
      provenance; models partition = EXACTLY the wake pack; **owner 2026-07-17: the pack
      is MULTI-model** — one wake model per unit, ≥3 near-term; whole pack in the
      partition for hash-verifiability, per-unit model + room identity provisioned
      post-flash via a **workbench-hosted management page over a firmware REST API** —
      filed onto DES-3's agenda; D-10 byte-identity stays whole-pack/wake-only). Owner
      rulings recorded: power **USB-C only** (Li-ion path unused, no cell), enclosure
      posture **wall-mounted**.
      **(c)** phase consequences: no `boards/waveshare-lcd146/` PCB project; **FW-1's
      `HW-GATED` marker dropped** (hardware adopted AND on the desk; sole remaining gate
      DES-3); DES-3 agenda expanded (REST API surface + management page + admin-UI
      shrink). Findings doc grew **§2.6** (owner-requested pre-designed-enclosure survey:
      Waveshare sells no 1.46 case; the whole community field is 3 mesh-only finds, none
      wall-mounted → the case is designed from the vendor STEP; snap-fit bezel + M2-boss
      mounting proven practical by the finds). docs: none — design-phase corpus (dossier
      + amendments are ledger-indexed ground truth, not manifest nodes; `quickstart` /
      `flash-and-provision` stay pending-gate on FW-1 first light; CONTRIBUTING's
      `devices` coverage description unchanged).
- [x] **DES-8** [dev:waveshare-lcd146] — **DONE 2026-07-18** — **Voice-satellite
      enclosure design AGREED** (interactive owner session; design doc
      `docs/design/satellite_enclosure.md` + parametric CAD
      `enclosures/waveshare-lcd146/case.py`, both committed; v0 exports build clean —
      squircle 45.1 × 48.5 face, **15.9 mm off the wall**). Owner decisions C-1..C-9:
      build123d toolchain (install = **INFRA-2**), keyhole wall mount (metal kept below
      the antenna band), cable exit **variant B** straight-plug open bottom (cable
      purchase settled: straight data-capable A-to-C + 5 V/2 A USB-A adapters ×3),
      squircle body, bottom-only openings, matte white PETG, Ø38.2 bezel lip outside
      the Ø37.36 viewing circle, two-part shell+plate, switch service pinholes.
      Prerequisite discharged: vendor pack re-downloaded, RAR/STEP/PDF all matching the
      findings §2.1 hashes. STEP survey (build123d) measured everything the CAD
      consumes — incl. the three SMTSO-M2-3.5 standoffs at (12.00, −14.95) /
      (−11.54, −15.45) / (0.00, +17.75) — and resolved the §2.5 posture consequence:
      BOTH transducers are soldered to the back face and fire at the wall → the sealed
      90°-duct-to-bottom-edge acoustic architecture (§3 of the design).
      **In-session correction (owner catch):** the speaker was first mis-read as
      wired/relocatable from the schematic 2-pin symbol — the STEP hierarchy proves it
      pad-soldered at (+11.17, 0.00), a PCBA child like the mic; concept + design
      corrected before agreement (the dossier's "onboard speaker" was right all
      along). Antenna keep-out resolved by construction (plastic-only case; keyholes
      at y −6). Follow-up filed: **DES-9** (HW-GATED print/fit/acoustic bench).
      docs: none — design-phase corpus, ledger-indexed; no `docs/manifest.json` node.
      contracts: none — mechanical design, no cross-repo surface (vendor STEP is
      hash-pinned reference data, not a Locveil contract).

## DOC — documentation

- [x] **DOC-1** — **DONE 2026-07-17** (filed + executed same session; owner-filed —
      first task of the new `DOC` prefix, prefix added to CLAUDE.md in the same change).
      **Deck-corpus audit: does `deck-common.md` truly contain the common pieces?**
      Claim-by-claim pass over deck-common §1–§7 against the four deck dossiers (owner
      ground rule: on contradiction the dossiers win; waveshare dossier out of scope),
      chip claims re-verified against official Espressif docs via the docs MCP.
      Evidence: **`docs/review/doc1-deck-corpus-audit.md`**. Verdict: structurally sound
      (no device truth leaked into common; §4/§6/§7 conventions genuinely family-wide;
      §5 chip truths all re-confirmed), but **2 contradictions** (F-1 "deck-derived
      only" vs FS90's sanctioned isolation-gate fallback; F-2 reservoir topology vs
      B215's bench-proven feed-series wiring — common's R-in-cap-branch factoring also
      electrically defeats its own low-ESR argument), **1 wrong chip figure** (F-5:
      "≈15 mA" light-sleep is the ESP8266 modem-sleep DTIM3 number; official ESP32
      auto-light-sleep = 2.2–3.3 mA — conservative, so nothing unsafe), **1 stale
      referent** (F-6: "legacy pin choices in the dossiers" — no dossier carries any),
      and **2 B215 gaps** vs common rules (F-3 missing 150 mA-rail fuse; F-4 missing
      per-unit ground-vs-earth meter check). Remediation filed as **DOC-2**
      (`review-then-remediate`). docs: none — review evidence + ledger only; the corpus
      fixes themselves land with DOC-2.

## PCB — board projects

## FW — firmware

- [x] **FW-2** [fleet] — **DONE 2026-07-18** — **esp-tflite-micro v6.0.2 compat spike:
      verdict PASS — FW-1 proceeds on IDF v6.0.2** (E-2 outcome; the v5.5.4 bail-out
      retired unused). Keeper harness `firmware/tflm-compat/` (the FW tree's first
      project; becomes the wake-stack component's standing build test at FW-1): TFLM
      core (MicroInterpreter + resolver + int8 micro_speech-scale invoke,
      DepthwiseConv2D/FullyConnected/Softmax/Reshape) + the full signal-lib feature
      path (18 preprocessor ops — Window/FftAutoScale/Rfft/Energy/FilterBank*/PCAN →
      kissfft), models vendored from the component's own micro_speech example
      (Apache-2.0, provenance in-file). Build: 1309/1309 steps, **0 errors**, clean
      link, 370 KB image; 17 benign `-Wshadow` warnings in TFLM reference kernels.
      Pin: exact `==1.3.7` in `idf_component.yml` + committed `dependencies.lock`
      (component_hash `22fc501a…`, esp-nn 1.2.3, idf 6.0.2, esp32s3). Datapoint
      reported upstream per the pass outcome: espressif/esp-tflite-micro#125 comment
      (2026-07-18) — the v6 gap is the examples layer, not the core. **Reconciliation
      find, carried to FW-1 intake:** the task-named "TFLite-Micro micro-features
      frontend" (`tensorflow/lite/experimental/microfrontend`, the lib ESPHome's
      microWakeWord uses) is NOT in the 1.3.7 distribution — removed upstream, the
      component's CMake GLOB of it is vestigial (also reported in the #125 comment);
      the port either vendors that C lib or moves features to the shipped signal lib
      (decide against the wake-pack models' feature semantics). Compile+link is the
      recorded gate; an on-bench invoke run is a bonus check left to FW-1 bring-up.
      docs: none — firmware spike + design/ledger records, no `docs/manifest.json`
      node touched. contracts: none — third-party registry dependency pinned
      (`espressif/esp-tflite-micro`, not a Locveil cross-repo surface; the wake-pack
      pin is untouched).

## INFRA — dev-machine / environment infrastructure

- [x] **INFRA-1** [fleet] — **DONE 2026-07-17** — **Install ESP-IDF v6.0.2** (DES-3
      decision E-2; the old v5.5.0 install + `~/.espressif` were deleted first, owner
      instruction, ~4.1 GB reclaimed). Executed: **shallow clone at tag `v6.0.2`**
      (`--depth 1 --recursive --shallow-submodules`, 691 MB — ~1 GB under the old full
      tree; 21 submodules) → `~/esp/v6.0.2/esp-idf`; `./install.sh esp32s3`.
      **Machine wrinkle found + worked around:** the system `python3` is a custom
      `/usr/local` 3.11.4 built WITHOUT the lzma module — the first install run died
      unpacking `.tar.xz` tools (`tarfile.CompressionError`); re-ran with
      `PATH="/usr/bin:$PATH"` (distro Python 3.12.3, lzma OK) → venv
      `idf6.0_py3.12_env`. **The same PATH prefix is required every time `export.sh`
      is sourced on this machine** (it probes bare `python3`) — noted for FW-2/FW-1
      sessions. Verified per the task's criterion: `idf.py --version` →
      **ESP-IDF v6.0.2**; `xtensa-esp-elf-gcc` 15.2.0 (crosstool-NG esp-15.2.0_20251204).
      Post-install cleanup (owner instruction): `~/.espressif/dist` archives (606 MB) +
      pip cache (1.2 GB) removed. Final footprint: 692 MB source + 4.1 GB tools/venv.
      **FW-2 (the compat spike) is now unblocked.** docs: none — dev-machine
      infrastructure, no user-facing surface.
- [x] **INFRA-2** — **DONE 2026-07-18** (filed + executed same session, DES-8 first
      act; owner: build123d over CadQuery/OpenSCAD — OCCT kernel, native STEP import;
      machine-level install as its own INFRA task per INFRA-1 precedent, over a repo
      venv). **build123d 0.11.1 installed** in a dedicated venv at
      `~/cad/build123d-env`, created from the DISTRO python (`/usr/bin/python3`
      3.12.3 — the lzma-less `/usr/local` wrinkle sidestepped at venv creation; OCP
      kernel wheel `cadquery_ocp_novtk 7.9.3`). Verified: version import + solid →
      STEP export → re-import round-trip exact. Use: `~/cad/build123d-env/bin/python`
      (no activation needed). Vendor mechanical pack re-downloaded to
      `~/cad/waveshare-lcd146/` and hash-verified against findings §2.1 (RAR
      `4647210e…`, STEP `0587a096…`, PDF `ff0da267…`) — the DES-8 prerequisite,
      discharged here since it lives machine-side with the tool. docs: none —
      machine-side toolchain. contracts: none — dev-machine install, no cross-repo
      surface.

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
- [x] **OPS-10** [fleet] — **DONE 2026-07-16** (filed + executed same session;
      adopt-on-re-pin per `ledger-discipline.md` §3/§6 — a consumer choice, not a
      delegation). **scope-guard re-pinned scope-v5 → scope-v6 (1.2.0 → 1.3.0).** Gains
      the HK-10/IMPL-2 `UNREFERENCED evidence` check (a doc under `[evidence] dirs` that
      no active/DONE ledger entry references = forgotten scope; consumer default warn).
      Vendored byte-identical from commons `scope-v6:packages/scope-guard/scope_guard.py`;
      toml header comment updated; no new config keys — `unreferenced` left at the
      consumer default (warn). First check green, 0 warnings: both evidence dirs
      (`docs/design/`, `docs/review/`) fully ledger-referenced at re-pin time.
      docs: none — vendored tool only.
- [x] **OPS-11** [fleet] — **DONE 2026-07-18** (PROD-26/HK-12 delegation lead; decision of
      record: HK-12 in `../locveil-commons/board/BOARD_DONE.md`; sub-tasks OPS-12 +
      OPS-13, each its own commit). **(a) Both greenlit repo-to-repo filings executed,
      committed and pushed in the sibling ledgers** — voice **BUILD-44** (`92b7178`, the
      wake-pack-v1.x bump confirmation: multi-model pack per DES-7 must land as a tagged
      bump, never out-of-band; `[deferred]` at filing, voice retags at intake; same-day
      addendum `c115340` — the OPS-13 smoke test found the published pack ALREADY drifted
      via HF mutable-ref URLs) and bridge **VWB-42** (`4cbf667`, the
      `device-integration-v1.1` minor-tag request at the VWB-41-normalized STAMP — DES-4
      needs clean tag bytes). **(b) Born-stamped clauses landed** ("contract surface —
      STAMP at first ship"): DES-5 task text (the broker verb surface) + the D-16 Stage-2
      REST API (`esp32_satellite.md` D-16 + `fw_execution_layer.md` E-4) — the scope-v7.1
      `contracts:` verdict line enforces the answer at their completions. **(c) Write-back:**
      lead ID + sub-IDs + filing IDs recorded in PROD-26 (`../locveil-commons/board/BOARD.md`).
      docs: none — ledger/design/board process surfaces, no `docs/manifest.json` node
      touched. contracts: none — the filings REQUEST owner-side bumps (wake-pack v1.x,
      device-integration v1.1); the pins move by their own re-pin/first-pin tasks (the
      wake-pack re-pin at voice's cut; DES-4).
      **Guard + block sweep, one commit.** `scripts/scope_guard.py` re-vendored
      byte-identical @ **`scope-v7.1`** (1.3.0 → 1.4.0: CONTRACTS-VERDICT +
      UNKNOWN-PREFIX; `contracts_verdict_since = 2026-07-18` set — no DONE entry predating
      today needed a retro line) and `scripts/contract_guard.py` @ **`contract-guard-v3`**
      (1.1.0 → 3.0.0: ORPHAN-TAG, CONTENT-DRIFT, VENDORABLE-UNREGISTERED, `--relax-tags`);
      `.contract-guard.toml` added (product default: `vendorable_roots = []`); the
      **contract-triad** block pinned into CLAUDE.md (block-pin lane, stripped-content
      sha256 `a3fe8d6b…` matching the commons pin); hook gains `--relax-tags` (CI stays
      strict); the registry-README drift one-liner folded in (`contracts/README.md` said
      `contract-guard-v1` while running v2 — the HK-12 round-2 live find — now v3 with
      real bytes behind it); CI workflow comment + path filter updated. Both guards green
      on first run, 0 warnings. docs: none — guard tooling + registry/CLAUDE.md process
      surfaces, no `docs/manifest.json` node touched. contracts: none — re-vendored the
      commons-owned guard tools at newer tags (consumed copies, not first consumption;
      the `[[tool]]` staleness watch arrives with OPS-13).
- [x] **OPS-13** [fleet] — **DONE 2026-07-18** (PROD-26/HK-12 delegation, rides OPS-11).
      **repin adoption.** `scripts/repin.py` vendored byte-identical @ **`repin-v1`**
      (1.0.0, the promoted voice BUILD-24 engine); `.repin.toml` written — families
      **ws-protocol**, **wake-pack** (sidecar-STAMP shape: files = the pinned STAMP,
      tag-only freshness, HF revision explicitly out of scope), **device-integration**
      (declared ahead of the first pin — DES-4 takes it at the VWB-42-requested v1.1 tag;
      never-pinned nags advisory until then) + the `[[tool]]` manifest (scope-guard @
      scope-v7.1, contract-guard @ contract-guard-v3, repin @ repin-v1);
      `default_fail_on = "none"` — the §5 recorded satellite carve-out, advisory until FW
      first light. Hook warn stage (`--check --fail-on none || true`) + CI advisory stage
      in `contract-guard.yml`. `publish_model_pack.py` grew the internal freshness gate:
      `publish` hard-fails on ANY wake-pack staleness (publishing IS touch-the-family —
      closes the publishes-without-committing gap), `verify` warn-only (offline bench
      legal). First live `--check`: both pins current, all three tools current, exactly
      the designed device-integration never-pinned warning. **Live find during the verify
      smoke test:** the published pack has ALREADY drifted upstream — HF `/resolve/main/`
      `irina.json` no longer matches the pinned sha256 (`.tflite` still matches; the
      STAMP's URLs are a mutable ref) — reported to voice as the BUILD-44 addendum
      (voice `c115340`): re-stamp at the bump + switch to immutable revision URLs.
      docs: none — consumer tooling/config, no `docs/manifest.json` node touched.
      contracts: **repin FIRST CONSUMED** (commons surface, vendored @ `repin-v1` with
      its `[[tool]]` self-watch); no owned surface moved.

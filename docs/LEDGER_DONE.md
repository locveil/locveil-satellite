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
- [x] **OPS-12** [fleet] — **DONE 2026-07-18** (PROD-26/HK-12 delegation, rides OPS-11).
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
- [x] **OPS-14** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 delegation
      LEAD; decision of record: HK-13 in `../locveil-commons/board/BOARD_DONE.md`;
      normative text `../locveil-commons/process/contracts.md` §1–§5). **Single-sourced
      contract graph — the satellite share is discharged.** Sub-tasks, each its own
      commit, all in DONE: **OPS-15** (`esp32-site-v1.1.0`, STAMP declares `artifacts`;
      re-pin owed: voice), **OPS-16** (contract-guard CI un-gated), **OPS-17** (tool
      sweep: repin v2, contract-guard v4, scope-v7.3.0; `.repin.toml` migrated;
      touch-the-family hard in CI), **OPS-18** (`docs-manifest-schema` first pin;
      internal `docs-manifest` STAMP retired), **OPS-19** + **OPS-20** (ws-protocol at
      `v1.0.1`, then the machine core at `v1.1.0`), **OPS-21** (wake-pack at `v1.0.1`),
      plus the follow-ups **OPS-22** (OPS-12 DONE header restored), **OPS-23**
      (scope-v7.3.1 block re-pin) and **OPS-24** (`consumer-pins` invariant re-truthed,
      owner-approved). **Amended in place and still open by design:** DES-4 (first
      `device-integration` pin at bridge's `v1.2.0`, set read from that STAMP, family
      re-declared with pin + test in one change; `[release]`, keeper dissent recorded in
      HK-13) and FW-1a (owns the ws-protocol conformance test over the pinned fixtures,
      gated on nothing; carries the v1.1.0 intake notes R-30 / R-25 / R-10).
      **Write-back:** lead ID OPS-14 recorded in PROD-28 by the coordinator session
      (verified in `../locveil-commons/board/BOARD.md`; the board is never edited from
      here). **Intake reconciliation of record (2026-10-05):** the esp32-site STAMP had
      no `artifacts`, a live header-path nit and two stale "voice pinned pre-tag"
      claims; the vendored tools trailed on two with no task filed; the CI un-gate was
      wave 0, not sweep work; the "no git tag" registry line was false
      (`docs-manifest-v1` exists); every `.repin.toml` conformance value was prose;
      bridge's `device-integration-v1.1` was unpinnable under the reserved-names rule.
      **End state:** every owned STAMP declares its artifacts and is three-part; every
      pin's file set is the owner's enumeration; no `files` list, no prose pointer and
      no historical version string left in config or registry; guard v4 strict green
      with one warning (`PIN-NO-CONFORMANCE`, ws-protocol — clears when FW-1a adds its
      test); `repin --check --fail-on any` clean. docs: none at the lead — the
      sub-tasks carry their own verdicts (esp32-site-reference at OPS-15, contributing
      at OPS-18). contracts: none at the lead — every move is recorded on its sub-task
      (owned: `esp32-site-v1.1.0`, re-pin owed: voice; consumed: ws-protocol `v1.1.0`,
      wake-pack `v1.0.1`, docs-manifest-schema `v1.0.0` first consumed).
- [x] **OPS-15** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      delegation (a), under lead OPS-14). **`esp32-site-v1.1.0` — standalone cut, STAMP
      declares `artifacts`.** Not riding DES-5 (its read-surface bump takes the next
      version). `contracts/esp32-site/STAMP.json`: `version` `1.1.0`, tag
      `esp32-site-v1.1.0` (three-part from this cut; `esp32-site-v1` stays frozen),
      `artifacts: ["provisioning/ansible/templates/esp32-site.conf.j2"]` — the template
      only, repo-root path; the pointer README is never enumerated and the STAMP travels
      implicitly. The singular `artifact` pointer is kept (it resolves; the org shape
      for an owned-surface-elsewhere). Folded in: the template header comment now names
      its real path (`provisioning/ansible/templates/…` — the nit recorded-not-fixed
      since v1; no directive changed), and the two stale claims that voice "pinned
      pre-tag, fills version/tag at its next re-pin" (README consumer line + STAMP
      `note`) — voice's pin has carried `esp32-site-v1` since its BUILD-24 re-pin.
      README also gains the three-level bump rule and a changelog; the registry row
      carries exactly the current tag; the owner guard's docstring names the major-1
      surface instead of a historical tag. Level: minor per the delegation (the STAMP
      gains its declaration; the set voice pins — template + STAMP — is unchanged; the
      comment fix alone would have been a patch). Verified: `check_esp32_site.py` green
      (9 markers); contract-guard green strict once tagged (CONTENT-DRIFT now live for
      the template — tag bytes == HEAD). Bump flow per HK-12: artifact + STAMP in this
      one commit → annotated tag on it → commit and tag pushed together.
      docs: esp32-site-reference — the canonical-reference page re-truthed (version
      authority, consumer line, bump rule, changelog). contracts: `esp32-site-v1.1.0`
      cut (minor — `artifacts` declared; header-comment bytes); re-pin owed: voice.
- [x] **OPS-16** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 wave 0, under
      lead OPS-14). **`contract-guard.yml` un-gated — every push and PR, no path gate.**
      Both 13-entry `paths:` lists removed (`contracts.md` §4 as amended: the owned
      artifact lives outside `contracts/`, so a gated job was one hand-kept copy of the
      edge away from never running for the edit the drift rule exists to catch); push
      trigger widened from `main` to every branch (`branches: ["**"]` — branch refs
      only, so a contract tag push does not start a second run); `pull_request`
      unfiltered. Steps unchanged: layer 1 strict, the advisory `repin --check` stage,
      both layer-2 owner guards — so layer 2 now also runs on every push. Reconciled at
      intake: PROD-28 lists the un-gate inside the satellite sweep AND as wave 0
      ("independent of everything else") — executed as wave 0. `ledger-guard.yml` keeps
      its path gate (prescribed by the shared-invariants block; outside this
      delegation). The registry's Guards paragraph said "path-gated" — re-truthed in
      the same change (its vendored-tool tag mention stays for OPS-17). Verification:
      trigger block parsed (`push.branches ["**"]`, bare `pull_request`); this commit's
      own pushed run is watched to completion and its verdict goes into the lead's
      write-back, not pre-asserted here (the OPS-8 lesson) — and since this commit
      touches formerly-listed paths, the first run the old gate would have SKIPPED is
      the next push that touches none of them. docs: none — CI workflow + registry prose, no
      `docs/manifest.json` node touched. contracts: none — enforcement wiring only, no
      versioned surface moved.
- [x] **OPS-17** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      delegation (b), under lead OPS-14). **The HK-13 tool sweep — one commit.**
      **Re-vendored through repin v2** (`repin.py tool <name>`, bootstrapped once from
      the commons copy; each compared byte-identical to its commons tag):
      `scripts/repin.py` @ **`repin-v2.0.0`** (1.0.0 → 2.0.0: pin set derived from the
      owner STAMP, three severity levels, `--touched`, tool re-vendor + hash),
      `scripts/contract_guard.py` @ **`contract-guard-v4.0.0`** (3.0.0 → 4.0.0: the
      HK-13 rule set; skips v3.1), `scripts/scope_guard.py` @ **`scope-v7.3.0`** (1.4.0 →
      1.4.1 — the v7.2 rotation fix; v7.3.0 itself is block-only). **Block:** the
      re-worded `contract-triad` block pinned verbatim into CLAUDE.md (marker
      `scope-v7.3.0`), sha256 `527e6888…` in `.scope-guard.toml`, equal to the commons
      pin; the other two blocks compared identical to their commons sources, untouched.
      **`.repin.toml` migrated:** every `files` list dropped; each `[[tool]]` carries
      `path` + `pinned_tag` + `sha256`; wake-pack `conformance =
      "scripts/publish_model_pack.py"` (a real path; its internal freshness gate still
      calls the same CLI — checked against v2's flags); ws-protocol carries NO
      `conformance` until FW-1a writes the test; the ahead-of-pin `device-integration`
      family removed until DES-4 (both per the intake rulings). **Registry:** Guards
      paragraph at the current tool tag, its historical "said v1 while running v2" aside
      removed (REGISTRY-VERSION failed on both strings on the first v4 run — the rule
      working as designed); pending-pin paragraph names `device-integration-v1.2.0` and
      says why the family is undeclared. **CI:** `fetch-depth: 0` + explicit tag fetch;
      `repin --check --touched "$BASE"` (push: `github.event.before`; PR: the base
      branch) — staleness stays advisory under `default_fail_on = "none"`, **touch-the-
      family is a hard failure from this commit** (FW-1a has not started, so this is
      earlier than the offer); steps named, names with ": " quoted. **Narrowed at
      execution:** the two pin-README trims and the two registry pin rows moved to
      their re-pin tasks (OPS-19, OPS-21) — editing a pin folder while its pin trails
      is precisely what the new CI step fails; the `check_esp32_site.py` docstring was
      already done in OPS-15. Verified: scope-guard green; contract-guard v4 green with
      5 warnings, all legacy-by-design and each owned by an open task (docs-manifest
      STAMP without `artifacts` → OPS-18; both pins' pre-HK-13 STAMPs and prose
      `conformance` → OPS-19 / OPS-21); `repin --check` reports both voice pins one
      patch behind and all three tools current with matching hashes. docs: none —
      vendored tooling, config, CI and registry prose; no `docs/manifest.json` node
      touched. contracts: none — consumed tools re-vendored at newer tags
      (`scope-v7.3.0`, `contract-guard-v4.0.0`, `repin-v2.0.0`; not first consumption);
      no owned surface moved, no pin moved.
- [x] **OPS-18** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      sweep, decision 6; under lead OPS-14). **`docs-manifest-schema` pinned; the
      internal `docs-manifest` contract retired.** **First pin**
      `contracts/pins/docs-manifest-schema/` at commons `docs-manifest-schema-v1.0.0`
      (`99e0d38`) via `scripts/repin.py docs-manifest-schema` — the set is the owner
      STAMP's: `manifest.schema.json` + the STAMP; strict PIN, `conformance =
      "scripts/check_docs_manifest.py"`; `[[family]]` added to `.repin.toml` (no `files`),
      registry row added, consumer why-note README in the pin folder.
      **`scripts/check_docs_manifest.py` no longer mirrors the vocabulary** — top-level
      and node key sets, the class / audience / status / phase enums, the id pattern, the
      surfaces cap and the `canonical` key set are all READ from the pinned schema, so
      there is no hand copy left to drift (one step past the delegation's floor of
      "check the mirror against the schema"); a missing or reshaped schema fails loudly.
      One behaviour change follows from reading the schema instead of the mirror: the
      optional top-level `$comment` key the schema always allowed is now accepted.
      Stdlib has no JSON-Schema validator, so the schema's rule KINDS are still applied
      by hand — recorded in the script and the pin README as the re-pin caveat.
      Negative-tested: bogus class, invented node field and unknown top-level key each
      fail; absent schema fails; real manifest green (7 nodes, 5/5 floor classes).
      **Retired:** `contracts/docs-manifest/` (STAMP + README) deleted — `docs/manifest.json`
      is instance data (`contracts.md` §1); the git tag `docs-manifest-v1` stays as
      frozen history; the registry's "Internal" section is gone and with it the false
      "no git tag" line (the tag existed all along — HK-13's recorded correction); the
      guard's stamp-coherence block removed. The manifest guard is now hermetic by
      construction: hook and CI need no commons checkout, and the retired STAMP's
      `schema` pointer (`../locveil-commons/…`, resolvable nowhere in CI) is gone.
      CONTRIBUTING.md's schema pointer re-truthed to the pin in the same change (caused
      staleness). Verified: contract-guard v4 green with exactly one warning
      (`PIN-NO-CONFORMANCE` on ws-protocol, by design until FW-1a); `repin --check
      --fail-on any` exits 0. docs: contributing — the schema pointer in the Docs
      discipline section now names the pin. contracts: `docs-manifest-schema` FIRST
      CONSUMED (commons surface, pinned @ `docs-manifest-schema-v1.0.0`); owned internal
      `docs-manifest` STAMP retired (no tag cut; `docs-manifest-v1` frozen) — nothing
      consumed it, no re-pin owed.
- [x] **OPS-19** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      delegation (c), under lead OPS-14). **`ws-protocol` re-pinned `ws-protocol-v1` →
      `ws-protocol-v1.0.1`** via `scripts/repin.py ws-protocol` (repin v2; voice
      `12d9a05`). The pin set came from the OWNER's STAMP at the tag — `artifacts:
      ["docs/guides/websocket-api.md"]` + the STAMP — not from a list in this repo; the
      fresh PIN.json is strict under guard v4 and carries `conformance: null` (no test
      until FW-1a; guard warns `PIN-NO-CONFORMANCE`, nothing fails, no placeholder).
      What the patch moved in the pinned bytes: the guide's header now names the
      three-part tag and states that the served `protocol_version` is the MAJOR only;
      the Python sample's port 6000 → 8080; the STAMP gains `artifacts` and the
      post-layout-move `code_constant` path. **No wire change** — FW-1a's build
      contract is what it was. This is the pin that read "current" for months while
      both owner files had moved under an unmoved tag — the live find HK-13 opened on;
      whole-file enumeration plus STAMP-DRIFT on voice's side now make that state
      impossible to reach silently. Same commit (moved in from OPS-17): the pin README
      trimmed to the consumer's why-note — manual `git show >` re-pin recipe out, the
      stale "FW opens after DES-3" lines out, no version string left in it (PIN.json is
      the record), conformance named as FW-1a's; registry row at `ws-protocol-v1.0.1`
      with the FW-1 → FW-1a pointer. `ws-protocol-v1.1.0` (machine core) did not exist
      at execution, so OPS-20 stays open. Verified: contract-guard v4 green (the pin's
      two legacy warnings gone, replaced by the expected `PIN-NO-CONFORMANCE`);
      `repin --check` reports ws-protocol current; `--touched` over this change raises
      nothing (the pin is at the owner's newest). docs: none — pin + its consumer note +
      registry row; no `docs/manifest.json` node touched. contracts: `ws-protocol` pin
      moved `v1` → `v1.0.1` (patch, bytes only; consumed, not first consumption).
- [x] **OPS-20** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      delegation (c), decision 9; under lead OPS-14). **`ws-protocol` re-pinned
      `ws-protocol-v1.0.1` → `ws-protocol-v1.1.0` — the machine core is in the pin.**
      Via `scripts/repin.py ws-protocol` (voice `221c175`); the set came from the owner's
      STAMP — 12 enumerated artifacts + the STAMP, copied flat: the guide,
      `frames.golden.json`, nine `transcript.*.jsonl`, `ws-protocol.schema.json`. Strict
      PIN, `conformance: null` (FW-1a's test does not exist yet; `PIN-NO-CONFORMANCE`
      stays the honest warning). **Fixture check from the firmware's seat, before
      commit — nothing unusable:** `frames.golden.json` parses (20 frames, 110 cases:
      59 valid / 51 invalid, + 6 unknown-type + 4 malformed); every file name, frame
      name and case id fits `[a-z0-9._/-]`, ids are unique and stay unique after
      identifier mangling; every case id sits under its frame; every valid case carries
      its frame's required keys with the declared JSON types; every frame has its
      `…/unknown-field` case; every invalid client-frame case carries `expect`; all nine
      transcripts parse, open with a matching `meta` line, name only frames the golden
      file defines with the right channel/direction; the four FW-1a needs
      (`audio-batch`, `reply-burst`, `satellite-pair`, `reconnect`) exist; `seq` pairs
      and restarts at 1 on the reconnect; no BOM; UTF-8 with non-ASCII text as the guide
      warns. **One substantive read of the guide diff, recorded on FW-1a:** beyond the
      new section the guide now states what the server does — errors are terminal,
      unknown keys/types must be ignored (binding from this version), and reply audio
      is converted DOWN but never up, where the previous text promised audio "already
      converted to the rate you registered"; the FW-1 baseline's R-10 leaned on the old
      sentence. Filed as intake notes on FW-1a (R-30, R-25, R-10 + the test shape); the
      owner-agreed `fw1_requirements.md` is not edited by a pin task. Same commit: pin
      README rewritten around what the pin now holds and how FW-1a consumes it;
      registry row at `ws-protocol-v1.1.0`. Verified: contract-guard v4 strict green
      (the one expected warning); `repin --check --fail-on any` exits 0. docs: none —
      pin + its consumer note + registry row + ledger notes; no `docs/manifest.json`
      node touched. contracts: `ws-protocol` pin moved `v1.0.1` → `v1.1.0` (minor — the
      pinned set gains the machine core, 11 files; consumed, not first consumption).
- [x] **OPS-21** [fleet] [release] — **DONE 2026-10-05** (PROD-28 / HK-13 satellite
      sweep, under lead OPS-14). **`wake-pack` re-pinned `wake-pack-v1` →
      `wake-pack-v1.0.1`** via `scripts/repin.py wake-pack` (repin v2; voice `ba3745a`).
      Voice cut it with the HK-13 tag set after all (not riding ASSET-6): a
      declaration-only patch — the sidecar STAMP declares `artifacts: []` with a
      resolving `guard` pointer, so the derived pin set is the STAMP alone, as before.
      Compared at re-pin: the `pack` object (word, HF repo + revision, per-file URLs and
      sha256s) is identical to the v1 pin — no hash moved, so nothing published or
      flashed against v1 stops verifying. The fresh PIN.json is strict under guard v4
      and its `conformance` is the real path `scripts/publish_model_pack.py` (the
      flash-time half stays FW-1a's). Same commit (moved in from OPS-17): pin README
      trimmed — manual re-pin recipe out, no version string left in it, "FW-1" → FW-1a,
      the publish script named where "OPS-1" stood (the model-pack half became OPS-7);
      registry row at `wake-pack-v1.0.1`. **Not fixed by this cut, still open on voice's
      side (voice ASSET-6, `[deferred]` there — the BUILD-44 answer + drift addendum):**
      the STAMP's URLs remain mutable `/resolve/main/` refs, and the July OPS-13 find
      (upstream `irina.json` no longer matching the pinned sha256) is untouched by a
      patch that moves no pack bytes — not re-probed over the network today. Verified:
      contract-guard v4 green, the pin's two legacy warnings gone; `repin --check
      --fail-on any` exits 0 — every pin and vendored tool at its owner's newest.
      docs: none — pin + its consumer note + registry row; no `docs/manifest.json` node
      touched. contracts: `wake-pack` pin moved `v1` → `v1.0.1` (patch, declaration
      only; consumed, not first consumption).
- [x] **OPS-22** — **DONE 2026-10-05** (filed + executed same session; intake find of
      OPS-14, coordinator ruling: own task and commit). **OPS-12 DONE header restored.**
      Commit `4c56057` (OPS-11 DONE) had deleted the header line
      `- [x] **OPS-12** [fleet] — **DONE 2026-07-18** (PROD-26/HK-12 delegation, rides
      OPS-11).` — one line, not the two the filing guessed — leaving OPS-12's body as a
      trailing paragraph of OPS-11. Re-inserted verbatim from `b078c90`; the restored
      entry compares byte-identical to that commit's, OPS-11 again ends at its own
      `contracts:` verdict, and scope-guard now counts OPS-12 as a completion. Nothing
      else in DONE touched. docs: none — ledger repair, no `docs/manifest.json` node
      touched. contracts: none — no surface involved.
- [x] **OPS-23** [fleet] [release] — **DONE 2026-10-05** (filed + executed same session;
      PROD-28 / HK-13 follow-up under lead OPS-14 — commons cut `scope-v7.3.1` in answer
      to the block disagreement this repo reported at the OPS-17 sweep). **scope-guard
      re-vendored `scope-v7.3.0` → `scope-v7.3.1`; contract-triad block re-pinned.**
      Block-only release: `scripts/scope_guard.py` bytes unchanged (same sha256
      `294cf411…`, byte-identical to the tag; `repin.py tool scope-guard` moved only the
      recorded `pinned_tag`). The block's enforcement line now reads "contract-guard and
      repin run in the hook and on EVERY push, no path gate (the ledger guard keeps its
      own)" where it said "both guards" — so it no longer contradicts the
      shared-invariants block's path-gated `ledger-guard` job, and this repo's
      `ledger-guard.yml` gate stands as wired. Verified before pinning: the tag is on
      commons' origin and its diff against `v7.3.0` in `process/claude-blocks/` is that
      one line. Copied verbatim between the markers (label `scope-v7.3.1`); sha256
      `eb3a35f5…` in `.scope-guard.toml`, equal to the commons pin. Registry: no edit —
      the Guards paragraph names no `scope-v*` string (only the contract-guard tag), so
      there was nothing to re-truth. NOT done here: the `consumer-pins` invariant edit
      (fourth pin) — repo-local law, left for the owner's own session (see OPS-14).
      Verified: scope-guard green; contract-guard v4 strict green, one warning
      (`PIN-NO-CONFORMANCE`, ws-protocol, by design); `repin --check --fail-on any`
      exits 0. docs: none — vendored tool record + pinned process block, no
      `docs/manifest.json` node touched. contracts: none — consumed tool tag re-vendored
      (`scope-v7.3.1`, bytes unchanged; not first consumption); no owned surface or pin
      moved.
- [x] **OPS-24** — **DONE 2026-10-05** (filed + executed same session; the discovered
      staleness recorded in OPS-14 at the OPS-18 close). **`consumer-pins` invariant
      re-truthed in CLAUDE.md — owner-approved edit to repo-local law** (owner,
      2026-10-05, on the coordinator's direct question: "I want these updates as a part
      of this run"). Two factual changes, nothing else in the invariant touched: the
      count and list gain the fourth pin — **commons `docs-manifest-schema`**, the
      vocabulary `docs/manifest.json` is validated against, pinned at
      `contracts/pins/docs-manifest-schema/` (OPS-18); and the device-integration bullet
      now says what the registry and DES-4 already say — not pinned yet, DES-4 takes the
      first pin at bridge's `device-integration-v1.2.0` (the lead sentence read as if
      all listed artifacts were pinned). The "left for the owner" note in OPS-14 is
      removed. docs: none — CLAUDE.md is agent-facing law, not a `docs/manifest.json`
      node. contracts: none — prose catching up with pins that already moved (OPS-18)
      or have not moved yet (DES-4).
- [x] **OPS-25** [fleet] [release] — **DONE 2026-10-05** (filed + executed same session;
      coordinator-relayed re-pin after voice's cut answering this repo's OPS-20 finding).
      **`ws-protocol` re-pinned `ws-protocol-v1.1.0` → `ws-protocol-v1.2.0`** via
      `scripts/repin.py ws-protocol` (voice `645100a`). Same twelve enumerated artifacts
      + STAMP; bytes moved in the guide and `frames.golden.json` only (the nine
      transcripts and the schema are unchanged); strict PIN, `conformance: null` as
      before. **What the minor carries, read from the pinned guide:** (1) the reply-audio
      guarantee withdrawn in v1.1.0 is RESTORED — the server converts to exactly the
      registered rate and channel count, up as well as down; "play it as it comes" is
      back, `speak_begin.rate`/`channels` always equal the registration, an
      unconvertible reply is not sent; (2) the case
      `reply.speak_begin/lower-rate-than-registered` is RETIRED, not removed — a retired
      case states nothing and a harness skips it; (3) new rule **T-9**: reply bursts
      never overlap; (4) the server type-checks opening frames — wrong JSON type =
      `error` + close on the two voice channels (18 new client-side `wrong-json-type`
      cases with `expect`, 16 of them on `audio.register` / `reply.register-reply`).
      Served `protocol_version` still "1". **FW-1a notes corrected in the same commit:**
      the R-10 note from OPS-20 is WITHDRAWN (baseline R-10 stands as the owner agreed
      it — no per-burst re-clock, no resampling); added: skip retired cases, T-9 may be
      relied on, send-side JSON types; R-30 and R-25 notes stand. **Fixture check from
      the firmware's seat, re-run before commit — nothing unusable:** golden file parses
      (20 frames; 129 frame cases + 6 unknown + 4 malformed = 139; live: 59 valid / 69
      invalid; 1 retired, carrying its retirement note); all names within
      `[a-z0-9._/-]`, unique, unique after identifier mangling; every non-retired valid
      case carries its required keys with the declared JSON types; every frame keeps a
      live `…/unknown-field` case; every client-side invalid case has `expect`, no
      server-side case does; all nine transcripts parse and satisfy T-2/T-3/T-4/T-9 and
      "speak_begin equals the registration" as replayed; the four FW-1a needs exist.
      One reading note recorded for FW-1a rather than a defect: the valid case
      `reply.speak_begin/two-channels` (22050 Hz, 2 channels) is a must-ACCEPT at the
      parser; on a connection registered mono it cannot occur. Same commit: registry row
      at `ws-protocol-v1.2.0`; pin README gains the skip-retired rule and stops
      hard-coding the T-rule count. Verified: contract-guard v4 strict green (the one
      expected warning); `repin --check --fail-on any` exits 0. docs: none — pin + its
      consumer note + registry row + ledger notes; no `docs/manifest.json` node touched.
      contracts: `ws-protocol` pin moved `v1.1.0` → `v1.2.0` (minor; consumed, not first
      consumption).

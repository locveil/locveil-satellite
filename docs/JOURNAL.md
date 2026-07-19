# locveil-satellite — journal (newest on top)

Dated record of work done; rotates per `ledger-discipline.md` §2 (whole days into
`docs/archive/journal/`, pointer here).

- **2026-07-18 — DES-8 filed: voice-satellite enclosure design (owner).** The DES-7
  mechanical inputs (findings §2: vendor STEP verified with hashes, not committed;
  §2.6: no vendor case, community finds unusable → design from the STEP) get their
  task. Wall-mounted, USB-C only/no battery pocket, cable-exit direction decided by
  the design (the owner's cable purchase pends on it). First act is the CAD toolchain
  decision — the repo has zero CAD tooling wired (no FreeCAD/OpenSCAD/CadQuery MCP or
  skill; `no-execution-toolchain-at-bootstrap` pattern, DES-2/DES-3 precedent);
  code-CAD (build123d/CadQuery with OCCT STEP import, or OpenSCAD) is the recorded
  candidate set for an agent-driven workflow. Antenna keep-out carried as the open
  mechanical unknown. Print/fabrication + bench fit-check follow-ups file from the
  design; only the fit-check is HW-GATED.

- **2026-07-19 — DES-8 delta 5: rightmost speaker slot was BLIND — owner caught it in
  their own STL viewer.** The corner-arc band migrates inboard with x: at the outer
  slot (x 14.2) the wall's cavity face sits at y −19.1, and the delta-4 cut box
  started at −19.6 — 0.48 mm left uncut, a pocket instead of a hole. (Their guess
  "mic soundpath" corrected en route: the three slots are the SPEAKER grille; the mic
  is the single Ø1.8 hole across the arc.) Cut boxes lengthened to y-10; probe
  coverage widened to what it should have been in delta 4 — EVERY aperture at three
  depths: 13/13 open, interference 0+0. `print/` + renders re-exported.

- **2026-07-19 — DES-8 delta 4: the owner's "they don't fit" was RIGHT — three fit
  defects found and fixed; fit is now machine-verified.** Suspected mirroring ruled
  out (features sit on matching sides; the exploded view reads as a clamshell but the
  plate TRANSLATES — R5 regenerated with straight assembly guides). The real defects,
  all from placing features by rectangle math against a squircle whose corner arcs
  pull the walls inboard: (1) top standoff pillar 0.16 into the shell top wall
  (cavity half-height mis-derived; r 2.6 → 2.3); (2) speaker rib corner at
  (19.85, 8.2) inside the cavity's corner-arc zone; (3) bottom apertures placed at
  the rectangular y −25.9 while the wall at those X lives on the corner arc — the
  MIC INLET CUT NOTHING (hole in air below the case) and the speaker slots never
  broke through. Fixes: apertures re-drilled through the real arc band (they exit on
  the under-curve), and a structural rule added — the plate solid is globally
  INTERSECTED with its outline prism, so no feature can ever overhang the rim again
  (first prism attempt decapitated the mic ring — caught by the ring-top assertion,
  −9.10 restored). Verification now part of the loop: 0 interference verts both
  directions, all five apertures probe OPEN through the wall, ring/rim/pillar
  assertions green. `print/` + renders re-exported; artifact updated (fit-verified).

- **2026-07-19 — DES-8 delta 3: mic gasket ring bug — owner's question caught it.**
  "What about the microphone gasket?" → re-walking the numbers showed the v0 ring
  grown to 0.5 shy of the BOARD plane, but the mic can sits 0.9 PROUD of the board —
  the printed ring would have crashed into the can. Seal plane corrected to the can's
  ported face (ring top verified at −9.10 = the 0.5 crush gap; outer trimmed to Ø4.4
  to land fully on the 4.7 × 5.0 can). Gasket spec recorded in the design §3
  (adhesive foam/silicone washer ~Ø4.5 × 0.8 → 0.5, bore Ø1.5); two DES-9 items
  added: mic PORT-OFFSET check (top-ported cans often have the hole off-centre) and
  sealing the duct's open side (v0 channel is a print-decision approximation).
  `print/` snapshots + renders re-exported per the folder rule.

- **2026-07-18 — DES-8 delta 2: print files + renders committed (owner request).**
  `enclosures/waveshare-lcd146/print/` — the v0 STL (slicer input) + STEP snapshots of
  both parts — and `renders/` — the five review PNGs — now live IN the repo, with a
  folder README fixing the rule: `case.py` is the source of truth, the snapshots are
  re-exported after any change, never hand-edited. DES-9 slices from `print/`.

- **2026-07-18 — DES-8 delta (same day, post-close): first renders generated — and they
  caught two v0 geometry bugs, fixed in `case.py`.** Owner asked for model + renders; a
  render path was added to the INFRA-2 venv (trimesh + matplotlib — shaded STL views;
  build123d's no-VTK kernel has no rasterizer) and five views published as a claude.ai
  render artifact. The pass immediately earned its keep: the speaker rib box overhung
  the back-plate rim by 1.2 mm on +X (the speaker sits 1.2 mm from the board edge — the
  shell could not have closed; ribs now asymmetric, right wall flush at the rim) and
  the top standoff pillar grazed the plate edge (r 3.0 → 2.6). Plate bounds verified
  ±19.98 after the fix. The DONE entry stays frozen; this line + the committed source
  carry the delta. DES-9's print starts from this corrected v0.

- **2026-07-18 — DES-8 DONE: enclosure design agreed — squircle wall case, 15.9 mm off
  the wall; DES-9 (print/fit/acoustics) filed; INFRA-2 DONE en route.** Interactive
  session. INFRA-2 executed first (owner: machine-level per INFRA-1 precedent):
  build123d 0.11.1 at `~/cad/build123d-env` from the distro python, STEP round-trip
  verified; vendor pack re-downloaded + all three §2.1 hashes matched. The STEP survey
  then MEASURED the design inputs (16 s import, 219 components): mic soldered at
  (−14.20, −12.05) back face, speaker pad-soldered at (+11.17, 0.00), SMTSO-M2-3.5
  standoffs exactly located, USB/switch/antenna zones fixed — resolving findings §2.5's
  posture question the hard way: BOTH transducers fire at the wall, so the case forms
  sealed gasket cavities in place with 90° ducts to bottom-edge openings. Concept sheet
  as a claude.ai artifact (S1 ground truth / S2 section / S3 cable variants / S4 body
  forms); owner decisions: keyholes, straight-plug open bottom (cable purchase settled:
  straight A-to-C + 5 V/2 A USB-A ×3), squircle, bottom-only openings, matte white
  PETG. **Session correction worth remembering: the speaker was briefly mis-read as a
  wired/relocatable part off the schematic's 2-pin symbol — the OWNER caught it against
  the wiki; the STEP hierarchy settled it (PCBA child, pad-soldered). Lesson: locate
  parts from the STEP hierarchy first, schematic symbols second.** Deliverables:
  `docs/design/satellite_enclosure.md` (AGREED, C-1..C-9) +
  `enclosures/waveshare-lcd146/case.py` (v0 builds + exports clean).

- **2026-07-18 — FW-2 DONE: the compat spike PASSES — FW-1 builds on IDF v6.0.2; the
  FW phase's first code committed.** The keeper harness (`firmware/tflm-compat/`)
  builds `esp-tflite-micro==1.3.7` clean on v6.0.2/esp32s3 — 0 errors, 370 KB image,
  17 benign `-Wshadow` warnings — exercising the TFLM core (int8 micro_speech-scale
  invoke) AND the full signal-lib feature path (18 preprocessor ops down to kissfft).
  The maintainer's "not updated for v6" (#125) turns out to be the EXAMPLES layer;
  the core is fine — datapoint posted upstream (#125, 2026-07-18), including a second
  find: the old micro-features frontend (`experimental/microfrontend`) is gone from
  the distribution entirely, the component CMake GLOB of it is vestigial. That
  frontend is what ESPHome's microWakeWord uses → FW-1 intake decision: vendor the C
  lib vs move features to the shipped signal lib (recorded in E-2's outcome note +
  FW-1's gate rider). Pin = exact `==1.3.7` + committed `dependencies.lock`. The
  v5.5.4 bail-out retires unused. Machine wrinkle held as recorded: `PATH="/usr/bin:
  $PATH"` before `export.sh`, then everything just works.

- **2026-07-18 — OPS-11 DONE: the PROD-26 delegation lead closes — filings, clauses,
  write-back all landed.** The two greenlit repo-to-repo filings executed and pushed
  (voice BUILD-44 `92b7178` + drift addendum `c115340`; bridge VWB-42 `4cbf667`);
  born-stamped clauses ("contract surface — STAMP at first ship") into the DES-5 task
  text (broker verb surface) and the D-16 Stage-2 REST API (`esp32_satellite.md` D-16 +
  `fw_execution_layer.md` E-4); the satellite write-back recorded in PROD-26 on the
  board (lead OPS-11, sub-IDs OPS-12/OPS-13, filing IDs). The full satellite delegation
  from HK-12 is now discharged: guards at scope-v7.1 / contract-guard-v3, verdict
  cutover live, contract-triad block pinned, repin adopted with the publish gate, drift
  one-liner fixed, filings out. Nothing here gated FW-2 (per the board's own sequencing
  note) — the spike remains the next FW step.

- **2026-07-18 — OPS-13 DONE: repin adopted — vendored @ repin-v1, `.repin.toml` live,
  publish flow gated; AND the smoke test caught real upstream drift.** The vendored tool
  + config (families ws-protocol / wake-pack / device-integration + the `[[tool]]`
  manifest watching scope-v7.1 / contract-guard-v3 / repin-v1), hook warn stage, CI
  advisory stage (`default_fail_on = "none"` — the §5 satellite carve-out until FW first
  light), and the `publish_model_pack.py` internal freshness gate (publish = touch-the-
  family = `--fail-on any`; verify warn-only so offline bench runs stay legal). First
  live `--check` green: both pins current, tools current, device-integration correctly
  nagging never-pinned (DES-4 pins at the VWB-42 v1.1 tag). Then the verify smoke test
  earned its keep immediately: HF `/resolve/main/irina.json` no longer matches the
  pinned sha256 (`.tflite` fine) — the STAMP's URLs are a MUTABLE ref and upstream
  moved; publish-from-URLs is now correctly impossible. Reported to voice same-day as
  the BUILD-44 addendum (`c115340`): re-stamp at the bump + immutable
  `/resolve/<revision>/` URLs.

- **2026-07-18 — OPS-12 DONE: guard + block sweep — scope-v7.1 + contract-guard-v3
  vendored, verdict cutover set, contract-triad block pinned, registry drift corrected.**
  One commit per the delegation shape. scope-guard 1.3.0 → 1.4.0 (CONTRACTS-VERDICT — the
  `contracts:` line required on completions from today; UNKNOWN-PREFIX — the satellite
  DOC-prefix scar, now failing loudly); contract-guard 1.1.0 → 3.0.0 (ORPHAN-TAG,
  CONTENT-DRIFT, VENDORABLE-UNREGISTERED, `--relax-tags` mid-bump tolerance — hook warns,
  CI strict); both byte-identical to their commons tags. `.contract-guard.toml` product
  default (`vendorable_roots = []`); third CLAUDE.md block (`contract-triad`) on the
  block-pin lane, hash verified against the commons pin. The `contracts/README.md` guards
  line said contract-guard-v1 while running v2 (HK-12 round-2 live find) — corrected to
  v3 in the same commit as the re-vendor. Both guards green on first run, 0 warnings.
  Earlier the same day, before the sweep commit: the two greenlit repo-to-repo filings
  executed — **bridge `4cbf667` (VWB-42**, the `device-integration-v1.1` minor-tag
  request) and **voice `92b7178` (BUILD-44**, the wake-pack-v1.x bump confirmation,
  `[deferred]` at filing since it gates no voice release — retag at their intake); both
  pushed.

- **2026-07-18 — PROD-26 delegation pulled: OPS-11 (lead) + OPS-12 (guard sweep) +
  OPS-13 (repin adoption) filed.** The HK-12 convention-enforcement-hardening execution
  entry landed on the board with the satellite delegation: guard sweep (contract-guard-v3
  + scope-v7.1 + `contracts_verdict_since` + the contract-triad block), repin adoption
  (vendored tool + `.repin.toml` + hook/CI warn stages + the `publish_model_pack.py`
  freshness check), the registry-README drift one-liner, born-stamped clauses for DES-5 +
  the D-16 Stage-2 API, and the two greenlit repo-to-repo filings (voice wake-pack-v1.x
  bump confirmation; bridge device-integration-v1.1 minor-tag request). Reconciled against
  repo reality at intake: the drift is live (`contracts/README.md` says contract-guard-v1,
  the vendored script is 1.1.0/v2, the CI workflow comment already says v2); commons
  facts verified against the tags (scope family newest is **scope-v7.1** — block-only
  release over v7, script bytes identical; block pin hash is the guard's stripped-content
  sha256, not the raw file hash). Sequencing per the commons notes: filings first, then
  the two sweep commits, clauses + write-back close OPS-11.

- **2026-07-17 — INFRA-1 DONE: ESP-IDF v6.0.2 installed and verified; FW-2 unblocked.**
  Shallow clone at tag v6.0.2 (691 MB, 21 submodules) into `~/esp/v6.0.2/esp-idf` +
  `install.sh esp32s3`. First run FAILED on a machine wrinkle worth remembering: the
  system `python3` is a custom /usr/local 3.11.4 built without lzma → tarfile
  CompressionError on the `.tar.xz` tool archives; re-run with `PATH="/usr/bin:$PATH"`
  (distro 3.12.3) succeeded, venv `idf6.0_py3.12_env` — and the SAME prefix is needed
  on every future `export.sh` source (it probes bare `python3`). Verified: `idf.py
  --version` = ESP-IDF v6.0.2, xtensa-esp-elf-gcc 15.2.0. Cleanup per owner: dist
  archives (606 MB) + pip cache (1.2 GB) removed; footprint 692 MB source + 4.1 GB
  tools/venv.

- **2026-07-17 — old ESP-IDF v5.5.0 install deleted (owner instruction, pre-INFRA-1).**
  `~/esp/v5.5/` (1.7 GB tree + the source zip) and `~/.espressif` (1.1 GB of v5.5-era
  toolchain/dist, no python_env) removed — ~4.1 GB reclaimed; `~/esp/` kept as the
  layout root for INFRA-1's v6.0.2 install. The E-2 bail-out re-anchored: fresh v5.5.4
  clone if ever triggered (INFRA-1 + FW-2 texts and `fw_execution_layer.md` E-2
  amended in this change).

- **2026-07-17 — FW-2 filed: the esp-tflite-micro compat spike as its own gating task.**
  Owner question "file the spike separately? what category?" → recommendation accepted:
  **FW** (it builds firmware code — the first in the repo; the harness is a keeper that
  becomes the wake-stack component's standing build test), not INFRA (installs only) or
  OPS (repo operations). Chain recorded: INFRA-1 → FW-2 → FW-1; FW-1 gains the gate
  note; the E-2 outcomes (pass→pin+report on #125 / fail→port+contribute /
  deep-port→v5.5.4 bail-out) carried into the task text, with the deep-port case
  closing FW-2 on the verdict and filing the port as its own follow-up.

- **2026-07-17 — DES-3 DONE: execution layer decided — native `idf.py`, IDF v6.0.2
  spike-gated; PlatformIO is out; FW gate lifts.** Interactive session; decision doc
  `docs/design/fw_execution_layer.md` (AGREED). Research findings: the 2024
  PIO/Espressif split froze Arduino only — official platform-espressif32 v7.0.1 builds
  espidf at IDF 6.0.1 but has never packaged 6.0.2 and sits outside Espressif's
  supported tooling; pioarduino is 5.5.4/Arduino-centric. Registry sweep: every FW-1
  dependency admits v6.0.x, with explicit v6 evidence for esp_lcd_spd2010 (2.0.0
  changelog), esp_websocket_client (IDF6 CI), esp_lvgl_port (IDF6 fixes) — EXCEPT
  `esp-tflite-micro` 1.3.7: CI tops at 5.5 and Espressif's maintainer confirmed v6
  incompatibility in the still-open issue #125 ("use release/v5.5 for now"). Owner
  decisions: native idf.py (no PIO, permanently); 6.0.2-first with the tflite-micro
  compat spike as the FW phase's first act — port-and-contribute if it fails, v5.5.4
  bail-out only if the port runs deep; toolchain install filed as INFRA-1 under the
  NEW `INFRA` prefix (registered in CLAUDE.md + scope-guard toml); D-16 Stage 2 goes
  REST-only on core esp_http_server (workbench page is the UI; Stage-1 portal stays,
  form may slip past v1 in favor of the NVS seed). Also defined: the background-monitor
  pattern (E-5) and the mandatory pin/strapping audit step (E-6 — waveshare-lcd146 §3
  already discharges it). v6.0 migration notes recorded (warnings-as-errors, mbedTLS
  4/PSA, cJSON to registry). FW section header updated: gate lifted, first act = the
  spike after INFRA-1.

- **2026-07-17 — DES-3 input: existing ESP-IDF v5.5.0 install verified on the dev
  machine; owner hardens the v6.0.2 preference.** Owner asked "I think I already have
  an older ESP-IDF — verify": found `~/esp/v5.5/esp-idf` (tag v5.5 @ `8c750b088`,
  2025-07-18, 1.7 GB) — source pristine (all 17,433 git 'modifications' are
  zip-extraction permission bits, 0 content changes; submodules complete) but the
  toolchain install is INCOMPLETE: only xtensa-gcc + gdbs extracted in `~/.espressif`,
  the rest sits unextracted in `dist/`, and `python_env` is missing → `idf.py`
  non-functional as-is; also 4 patches behind v5.5.4. Owner ruling folded into DES-3:
  strong preference for v6.0.2; the dependency-availability research is part of DES-3,
  and porting lagging modules to 6.0.2 + contributing upstream is a sanctioned outcome.
  Nothing installed/touched (`no-execution-toolchain-at-bootstrap` — DES-3's call).

- **2026-07-17 — DOC-1 DONE: deck-corpus audit (deck-common vs the four dossiers);
  DOC prefix born.** Owner-filed with the ground rule "dossiers win"; waveshare dossier
  untouched. Result (`docs/review/doc1-deck-corpus-audit.md`): common is structurally
  sound — pointers not leaked truth, §5 chip claims all re-verified against
  datasheet/TRM/IDF docs — but the audit found 2 genuine contradictions (F-1 absolute
  "deck-derived only" vs FS90's sanctioned external-supply fallback behind the
  isolation gate; F-2 common's resistor-in-cap-branch reservoir vs B215's bench-proven
  resistor-in-feed topology, which is also the electrically coherent one), 1 wrong chip
  figure (F-5: "≈15 mA" light-sleep idle is really the ESP8266 modem-sleep DTIM3
  number; official ESP32 auto-light-sleep is 2.2–3.3 mA — conservative, nothing
  unsafe), 1 stale referent (F-6: dossiers carry no legacy pins), and 2 B215 gaps
  (F-3 no fuse on its 150 mA rail; F-4 no per-unit ground-vs-earth check in its bench
  list). Remediation filed as DOC-2 per review-then-remediate. `DOC` prefix added to
  CLAUDE.md's ledger section (owner, documentation-corpus audits/maintenance) — and,
  caught right after the DOC-1 commit, registered in `.scope-guard.toml`'s `prefixes`
  too: the guard's prefix table proved DOC-blind (18 tasks counted, DOC-1/DOC-2
  invisible = unenforced), the toml is the repo-owned half of the vendored-guard
  contract, so the fix is config, not a guard edit.

- **2026-07-17 — post-close DES-7 owner amendment: all three listening animations ship,
  selected per unit.** Follow-on to the multi-model wake-pack discussion, same session:
  instead of hard-picking variant B, the display-enabled build compiles in all three
  mocked variants (A rings / B waveform / C rim arc — procedural renderers, tiny) and
  the active one is a per-unit NVS config enum set from the workbench management page,
  default B. Unlike the wake pack this is plain code + config — no artifact/pin/hash
  machinery. D-2 amendment re-worded in `esp32_satellite.md`; the page-surface note on
  DES-3 extended. The DONE entry stays frozen as written (single-pick was true at close);
  this journal line + the design doc carry the delta.

- **2026-07-17 — DES-7 DONE: voice-satellite hardware adopted — dossier + design
  amendments landed.** Interactive owner session. Slug fixed `waveshare-lcd146`; dossier
  written with the full pin/strapping map (schematic GPIO matrix + vendor demo @
  `fda89ff` + wiki, all three agreeing on every pin; strap audit vs the S3 datasheet/TRM
  found GPIO45/46 double as LCD QSPI DATA1/0 — vendor-designed-in, safe at reset,
  download-mode caution recorded; no amp-enable GPIO; the demo's stale `SD D3=21` define
  flagged). `esp32_satellite.md` amended: D-2 display-optional (+ the variant-B waveform
  animation spec; touch scope → FW-1 intake), D-7/D-8 (PCM5101A/NS8002; §14 v2 audio
  CLOSED on this hardware), D-9/D-12 (µVAD compiles into the app image; models
  partition = the wake pack only). Mid-session owner rulings: power USB-C only; posture
  wall-mounted; the wake pack is MULTI-model (one wake model per unit, ≥3 near-term) →
  whole pack in the partition, per-unit model + room identity provisioned post-flash via
  a WORKBENCH-hosted management page driving a firmware REST API — filed onto DES-3's
  agenda (API surface, on-device framework, D-16 admin-UI shrink). FW-1's `HW-GATED`
  marker dropped (hardware on hand; sole gate DES-3). Findings doc grew §2.6
  (owner-requested pre-designed-enclosure survey: no vendor case, 3 mesh-only community
  finds, none wall-mount → design from the vendor STEP).

- **2026-07-16 — DES-3 input sharpened: docs-MCP is latest-only; latest = IDF v6.0.2.**
  Owner question ("does the docs MCP only serve the latest IDF? which version is
  that?") answered with verification, folded into the findings doc as §3.5 + the DES-3
  ledger note: the espressif-docs MCP returns `en/latest` docs + `master` source only
  (checked via returned source URLs); latest stable is v6.0.2 (2026-06-29), 5.x ended
  at v5.5.4, Waveshare's 5.3.2 demo is two minors + a major behind but uses the same
  `i2s_std` API family, so it stays a valid wiring reference. Posture recorded for
  DES-3: target v6.0.x after an esp-tflite-micro + SPD2010-components compat check,
  v5.5.x fallback; the vendor demo proves the hardware, never anchors our version —
  the earlier "known-good IDF version anchor" phrasing corrected in the same change.

- **2026-07-16 — DES-7: hardware findings doc committed (enclosure data + vendor
  software survey).** `docs/design/assets/des7-hardware-findings.md`, referenced from
  DES-7 (input evidence) and DES-3 (decision input). Casing verdict: everything CAD
  needs exists — the wiki's structural-diagram RAR holds a dimensioned 2D print
  (39.36×41.53 board, 3× M2.0-H3.5 bosses fully dimensioned, 9.0 mm stack) AND a full
  3D STEP assembly (219 components incl. the mic body and the 12×10×2.8 speaker);
  vendor URLs + sha256s pinned in the doc, files not committed (15 MB). Mic confirmed
  TOP-ported (Waveshare-hosted datasheet + SnapEDA/DFRobot) → the D-7 acoustic channel
  is a gasket-sealed hole over the mic body, no through-PCB port. `waveshareteam`
  survey: the board repo carries a complete NATIVE ESP-IDF 5.3.2 project (SPD2010 +
  PCM5101 + mic capture with the 32-bit/RIGHT-slot wiring truth + TCA9554 reset
  gating + esp-sr wake demo proving the audio pipeline on this exact hardware, factory
  .bin for bench restore) — validates DES-3's native-idf.py option; espressif-maintained
  SPD2010 display+touch registry components exist, so the consumption model is registry
  drivers + own glue, no vendoring of the demo's UNLICENSED code (repo has no license
  file); no 1.46 BSP in Waveshare's components repo yet — watch item.

- **2026-07-16 — DES-7: listening animation decided — variant B "waveform".** Three
  candidates mocked as an interactive page simulating the round 412×412 screen
  (idle/listening states, synthetic speech-amplitude drive; LottieFiles' free tier
  turned out generation-gated, so the mockups were built directly): A pulse rings /
  B waveform / C rim arc. Owner picked **B** — five center-weighted rounded bars driven
  by the capture-frame speech envelope, cyan→violet on black; idle = dim near-static
  dots. Spec folded into DES-7 (b); mockup committed as
  `docs/design/assets/des7-listening-mockup.html` (all three variants kept for the
  record).

- **2026-07-16 — DES-7 scope expanded: µVAD provenance decided (compiled into the app
  image).** Owner question "wake models come from my HF account — what about microVAD on
  ESP32?" surfaced a real hole: D-9 names `pymicro-vad` but neither D-12 nor any
  contracts pin covers the VAD model's on-device provenance/storage. Verified facts:
  the desktop wheel (voice `.venv`, pymicro-vad 2.0.1) embeds the model in the compiled
  extension — no `.tflite` ships; the ESPHome reference distributes the same
  Ahrendt-lineage model as `vad.json`+`vad.tflite` (micro-wake-word-models v2, ~16 KB
  tensor arena). Owner decision folded into DES-7 (b): bake the VAD model into the
  firmware image (vendored third-party source, provenance in the component README) —
  the models partition stays exactly the wake pack, no fourth pin, no publish-flow
  extension; D-10 byte-identity stays wake-model-only; one-time byte-diff vs the wheel's
  model at FW build.

- **2026-07-16 — OPS-10 DONE: scope-guard re-pinned scope-v5 → scope-v6.** Found while
  sweeping the board for delegations and pin drift (result: no pending satellite
  delegations; both contract pins current at their owners' newest tags — `ws-protocol-v1`,
  `wake-pack-v1`; the DES-4 `device-integration-v1.1` request still fires at authoring
  time). scope-v6 = 1.3.0, the UNREFERENCED-evidence check (HK-10/IMPL-2). Vendored from
  the commons tag, toml header bumped, `unreferenced` left at the consumer default (warn).
  Green on first run, 0 warnings — every doc in `docs/design/` + `docs/review/` is
  ledger-referenced.

- **2026-07-16 — DES-7 filed: voice-satellite hardware is the Waveshare
  ESP32-S3-Touch-LCD-1.46B (owner decision).** Owner disclosed 3 units already on the
  desk (bought 2025) — the selection happened outside the repo; the corpus had zero
  mention of the board (exhaustive grep across satellite/voice/commons). Specs verified
  against the Waveshare wiki, official schematic, and demo code: S3R8 8 MB octal PSRAM +
  16 MB flash, single MSM261S4030H0R I2S mic, PCM5101A + NS8002 speaker path, SPD2010
  412×412 round touch LCD, Li-ion/USB-C. Fit against `esp32_satellite.md`: every v1
  requirement is met (mic class D-5, separate-I2S topology D-8, wake-pack flash
  partition D-12, OTA A/B). Two design tensions became DES-7 scope instead of blockers:
  D-2's "headless" amends to "display support OPTIONAL in firmware" (owner wants a
  minimal listening animation as a nice-to-have — the Siri-like idea, not Siri's UI),
  and the §14 v2 ES8311/AEC/2-mic path is CLOSED on this hardware (v2 = new hardware).
  Voice-satellite PCB phase collapses to none; FW-1's `HW-GATED` hardware-selection
  reason lifts once DES-7 lands (FW still gated on DES-3).

- **2026-07-15 — OPS-9 DONE: the PROD-25 one-liner was a dud — explicit tag fetch.**
  Watched OPS-8's pushed run instead of trusting it: FAILED, same 2× TAG-MISSING.
  `fetch-tags: true` is a no-op on checkout's default shallow single-commit fetch
  (actions/checkout#1467 — the flag only drops `--no-tags`; auto-following can't see
  tags on unfetched commits). The OPS-8 repro had passed because `clone --no-tags`
  isn't checkout's real fetch shape — this time reproduced from the EXACT state
  (init + single-sha depth-1 fetch) before trusting the fix. Fix: explicit
  `git fetch --tags --depth=1 origin` step; green locally from the exact state; the
  pushed run is monitored and its verdict lands in the board write-back.
  Blast radius filed back to PROD-25: commons' own post-fix run dd7c270
  failed identically (convention §4 prescribes the dead one-liner; commons workflow
  still broken), voice BUILD-38 was verified by simulation only.

- **2026-07-15 — OPS-8 DONE: contract-guard CI checkout fetches tags (PROD-25).**
  The v2 `TAG-MISSING` rule reads `git tag -l`, but `actions/checkout` defaults to a
  tag-less shallow clone — since OPS-5 re-vendored v2, this repo's guard job was
  latently broken: the next `contracts/**` push would have fired 2× false TAG-MISSING
  (`esp32-site-v1`, `docs-manifest-v1`), nothing wrong in the contracts. One-line fix
  per `process/contracts.md` §4: `fetch-tags: true` on the checkout (shallow stays
  fine). Both sides reproduced locally: tag-less clone fails exactly as CI would, tags
  make it green. Board text reconciled at intake — its "rides the v2 re-pin" framing
  was stale for satellite (re-pin already done); fix landed standalone. Stale v1 header
  comment in the workflow fixed in the same change. OPS-8 written back to PROD-25.

- **2026-07-14 — OPS-7 DONE: model-pack publish flow — hash-at-publish is machinery now.**
  `scripts/publish_model_pack.py` (stdlib-only, workstation-side — publish from where
  the pin lives; ssh/scp transport; outside the DES-5 broker, no CA key involved).
  Nothing lands in `/srv/esp32/models/<client_id>/` unless every file's sha256 matches
  `contracts/pins/wake-pack/STAMP.json`; drift on already-published files is refused
  (breaking change per the STAMP — pin bump then `--allow-replace`); re-runs idempotent;
  remote copies re-hashed post-copy. Verified live against the HF upstream (both hashes
  green) + the full local failure matrix; the ssh branch mirrors the local one and is
  untested until a controller session — recorded honestly in the DONE entry. README
  publish section rewritten around the tool (kept user-grade, no tracking refs — the
  OPS-4 rule); firmware publishing stays plain copies under dormant OPS-1. Sprint-01's
  0.3-session satellite row is thereby executed. docs: provisioning-runbook.
- **2026-07-14 — sprint-01 intake: OPS-1 split, OPS-7 filed (model-pack publish flow;
  the sprint row's "OPS-1a" renumbered).** The sprint-01 satellite row pulled
  (`../locveil-commons/board/sprints/sprint-01.md`, §4 partial-dependency split).
  Intake wrinkle, caught by the guard's own count: the coordinator pre-named the split
  half "OPS-1a", but scope-guard's declaration regex is numeric-only (`(PFX)-\d+\b`) —
  a letter-suffixed row parses as PROSE, invisible to ledger enforcement (it landed
  that way in `a181f5d` for ~one commit; the aliases table is numeric-only too, so no
  alias escape). Renumbered to **OPS-7** with the sprint-row name recorded in the task
  text. UPSTREAM FINDING to report to commons: sprints.md §4 says splits need "no new
  syntax", but the sprint machinery minted letter-suffix IDs its own guard can't parse —
  either §4 forbids them explicitly or scope-guard learns them; commons' call.
  Reconciled clean otherwise: the zero-dependency claim holds (pin `wake-pack-v1` +
  upstream HF artifacts + deployed `/srv/esp32/models/` layout; no FW/bench/hardware
  needed). OPS-7 takes the PROD-16 hash-at-publish amendment wholesale; OPS-1 narrows
  to the firmware half, dormant until FW-1 produces an image. Sprint side-finds disposition:
  the D-17/workbench-panel reconciliation was already discharged by the PROD-24 DES-5
  expansion (same day, `44d7646`); the DES-4 `device-integration-v1.1` wrinkle was
  already recorded at OPS-3 intake; the `process/sprints.md` §6 vacuous-line finding is
  a commons doc finding — becomes scope only if DES-3 is selected in a future sprint.

- **2026-07-14 — PROD-24 delegation pulled: DES-5 expanded (broker + verbs + operator
  credential), OPS-6 ansible earmark filed.** The Workbench shell council's satellite
  delegation: DES-5 (cert lifecycle) absorbs the privileged broker — one privileged code
  path, two peer clients (`esp32-provision` CLI + the workbench provisioning page); the
  owner overruled D-17's CLI-only reading (CA-key boundary survives, the SSH-only gate
  does not — D-17's second amendment lands via the expanded design), plus the full verb
  vocabulary (`list/status/approve/reject-pending` now, `revoke-issued/renew` from DES-5's
  original core) and the workstation operator-credential question (home-CA client cert vs
  separate secret). Reconciled clean: `provisioning/README.md` verbs match (today's
  `revoke` = the board's `reject-pending` — drop-pending only, exactly the gap DES-5 was
  filed on), D-17 already carried the "config-ui may call the same scripts later" hook,
  `provisioning/ansible/deploy.yml` exists as the OPS-6 target. OPS-6 filed as an EARMARK
  (owner: not this sprint; blocked on DES-5 by definition). Binding conditions recorded in
  the ledger: no write API before PROD-4's auth decision; the workbench page stays dormant
  until DES-5 + first light. IDs written back into the board's PROD-24 entry (commons
  commit). Normative source: `../locveil-commons/docs/design/workbench.md` §6.
- **2026-07-14 — OPS-5: contract-guard re-vendored @ v2 (PROD-22) — TAG-MISSING fired here too.** Third instance org-wide of the STAMP-names-a-nonexistent-tag false green; docs-manifest-v1 created at the STAMP's landing commit. Executed by the commons session on owner instruction; satellite added to the PROD-22 delegation list at execution (the original named bridge+voice only).
## 2026-07-12 — PROD-17 delegation pulled: user-docs convention adopted (OPS-4 filed + executed)

Unattended session, same pattern as OPS-3. All three delegation items under one ID:
the docs manifest born (`docs/manifest.json`, 7 nodes, `docs-manifest-v1` INTERNAL
stamp, coherence guard as pre-commit stage 4 + CI step), `CONTRIBUTING.md` created,
the provisioning-README user-grade pass done, scope-guard re-pinned `scope-v5`
(1.2.0, docs-verdict rule + the new shared-invariants block). Reconciliation notes:
the FW/PCB-gated doc classes went in as **pending-gate nodes** naming their gates
(`FW-1 first light`; deck builds gate on the first bench-verified board and
`derives_from` the `docs/devices/` dossiers) — declared, not written; the
canonical-reference floor slot is staffed by OPS-3's `esp32-site` surface (stamp +
guard already existed — the two delegations composed cleanly). Discovered-and-fixed
in the pass: the publish example still said `jarvis.*` (the pack is `irina`), and the
root README pointed users at the ledger. `docs_verdict_since` set to **2026-07-13**,
not today: the four completions dated 2026-07-12 predate the rule and DONE is frozen
history — the OPS-4 entry carries a voluntary verdict line anyway as the format
exemplar. Upstream nit reported in the board write-back: the commons skeleton
manifest's `$comment` key fails its own schema (`additionalProperties: false`).

## 2026-07-12 — PROD-16 delegation pulled: the contracts pins-shape cut (OPS-3 filed + executed; DES-4/OPS-1 amended)

Unattended session (owner approved the analysis, stepped away). Pulled the PROD-16
satellite delegation from the board; `task-start-reconciliation` produced four deltas
that reshaped execution: **(1)** `ws-protocol-v1` + `wake-pack-v1` were ALREADY tagged
(voice ARCH-47 executed the same afternoon, voice `9f371b9`) — the delegation's interim
"unstamped PIN.json now, stamp later" step collapsed; both pins landed stamped and
strict, and the WS doc had moved +17/−3 since our interim commit-ref pin (`98e8fd0`), so
the re-pin at the tag was substantive, not cosmetic. **(2)** `contracts/README.md` was
stale in all three rows, not just the one line the delegation named — replaced wholesale
by the §2 registry. **(3)** A reconciliation DISCOVERY: this repo OWNS a contract nobody
delegated — voice's registry pins our Plane-B nginx template (`esp32-site`, pre-tag
@ `37dcac5`, "version/tag fill in when the satellite stamps this surface") — stood the
owned surface up: STAMP + pointer README + tag `esp32-site-v1` (byte-identical to
voice's copy, verified) + day-one owner guard `scripts/check_esp32_site.py`; the
template's stale comment path (`nginx/` vs `provisioning/`) stays as recorded debt —
fixing a comment is a byte change is a version bump. **(4)** The bridge's
`device-integration-v1` tag carries the PRE-convention STAMP (core fix landed post-tag,
`eb08146`/VWB-41, no bump) — recorded as a DES-4 intake wrinkle with the preferred
`v1.1` repo-to-repo request; deliberately NOT filed into the bridge tonight (their
ledger, their session). Enforcement: `contract_guard.py` vendored @ `contract-guard-v1`,
CI job + three-stage pre-commit; both guards green, **0 warnings**. Ledger: OPS-3
straight to DONE (the DES-6 filed+executed pattern); DES-4 + OPS-1 amended in place;
IDs written back into the board's PROD-16 entry (commons commit).

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

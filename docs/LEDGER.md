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
| `docs/design/esp32_satellite.md` (DRAFT 2026-06-14; migrated from voice 2026-07-12, §4 wire tables demoted to the contracts pin) | the consolidated satellite design (voice ARCH-22 lineage) — FW-1, DES-4, DES-5 context |
| `docs/design/ws_esp32_transport.md` (SUPERSEDED by `esp32_satellite.md`; migrated frozen) | historical lineage only |
| `docs/devices/deck-common.md` + `revox-a77.md` / `revox-b215.md` / `pioneer-cld925.md` / `panasonic-fs90.md` (harmonized 2026-07-12) | per-device hardware ground truth — DES-4 descriptors, future `boards/<slug>/`, deck FW apps |
| `docs/devices/waveshare-lcd146.md` (2026-07-17) | voice-satellite hardware ground truth (DES-7) — DES-3's mandatory pin/strapping audit, FW-1, enclosure CAD |
| `docs/design/assets/des7-hardware-findings.md` (2026-07-16, enclosure survey added 2026-07-17) | DES-7 input evidence — enclosure data + `waveshareteam` survey; DES-3 decision input (§3.5); FW-1 consumption model |
| `docs/review/des1-truth-pass.md` (2026-07-12) | DES-1 evidence: conflict resolutions, REQUIREMENTS disposition (VWB-38 feed), code sweep, pin re-audit |
| `docs/review/doc1-deck-corpus-audit.md` (2026-07-17) | DOC-1 evidence: deck-common vs dossiers claim-by-claim audit — DOC-2 remediation feed |

## DES — design

- [ ] **DES-2** [fleet] — **skidl-skills review / rethink / adoption** (focused session,
      HK-4 round 4). Deliberately NOT installed at bootstrap
      (`no-execution-toolchain-at-bootstrap`); this task decides whether/how it enters the
      PCB toolchain alongside Serena-over-cloned-SKiDL.
- [ ] **DES-3** [fleet] — **Firmware execution-layer decision** — PlatformIO vs
      pioarduino-lineage vs native `idf.py`, including docs-MCP ↔ IDF-version alignment,
      the background-monitor pattern, and a **mandatory pin/strapping audit step**.
      **MANDATORY before any FW phase starts** (`phase-gates`). The
      PIO-platform-vs-latest-IDF tension is a fact-check, not a blind bet (HK-4 round 4).
      *(Decision input 2026-07-16, from the DES-7 hardware findings —
      `docs/design/assets/des7-hardware-findings.md` §3.1 + §3.5: the vendor's own
      reference for the adopted voice-satellite board is a plain-`idf.py` native project
      on IDF 5.3.2, validating the native option — but it proves the HARDWARE, not our
      version; demo pins LVGL ~8.3. Verified same day: the espressif-docs MCP serves
      `en/latest` + `master` source ONLY (no version-pinned docs), latest stable =
      **v6.0.2** (2026-06-29; 5.x ended at v5.5.4). Working posture: target v6.0.x —
      aligning firmware with what the docs MCP can fact-check — AFTER verifying
      `esp-tflite-micro` + the SPD2010 registry components against it; fallback v5.5.x;
      the i2s_std API family spans both, so the demo stays readable as a wiring
      reference either way.)*
      *(Decision input 2026-07-17, workstation recon + owner ruling: an **ESP-IDF v5.5.0
      install already exists on the dev machine** — `~/esp/v5.5/esp-idf` (tag v5.5 @
      `8c750b088`, source pristine — the 17k git "modifications" are zip-extraction
      permission bits only, submodules complete) with a PARTIAL toolchain in
      `~/.espressif` (xtensa esp-14.2.0 + gdbs extracted; cmake/ninja/openocd/clang/
      riscv-gcc downloaded to `dist/` but unextracted; **no `python_env`** — install.sh
      never completed, so `idf.py` is currently non-functional). It is also 4 patches
      behind its own line (v5.5.4). Owner ruling: **strong preference for v6.0.2** — the
      earlier "target v6.0.x" posture hardens; the library/module-availability research
      (esp-tflite-micro, esp_lcd_spd2010 + touch, and whatever else FW-1 pins, against
      v6.0.x) is IN-SCOPE for this task, and **where a needed module lags the major, we
      may port/upgrade it to 6.0.2 ourselves and CONTRIBUTE upstream** — a sanctioned
      outcome, not just a fallback trigger. The v5.5 install stays untouched until this
      task decides (finish it only if the compat check forces the v5.5.x fallback; the
      `~/esp/<version>/` layout accommodates a fresh v6.0.2 alongside).)*
      *(Owner agenda expansion 2026-07-17, DES-7 session: the wake pack is MULTI-model —
      one wake model per unit, ≥3 near-term — so per-unit model selection AND room
      identity are provisioned POST-flash through a **WORKBENCH-HOSTED device-management
      page** that drives the device over a **firmware REST API** (owner rulings
      2026-07-17). Post-close DES-7 amendment (owner 2026-07-17): the page's config
      surface also carries the **listening-animation variant** — all three mocked
      variants (A/B/C) compile into the display-enabled build, per-unit NVS enum,
      default B (plain config, no artifact machinery; D-2 as re-amended). DES-3 session subjects alongside the execution-layer decision: the
      REST API surface, its on-device framework, how far the D-16 Stage-2 on-device
      admin UI shrinks toward being just that API, and the page's relation to the DES-5
      broker/workbench surfaces. See the D-12 amendment in
      `docs/design/esp32_satellite.md`.)*
- [ ] **DES-4** [dev:revox-a77][dev:revox-b215][dev:pioneer-cld925][dev:panasonic-fs90] —
      **Adopt the bridge's device-descriptor format for the deck devices.** Consumes the
      bridge's device-integration-convention design (PROD-15 bridge delegation item 2;
      "convention down, descriptors up") — author the conforming per-device descriptors
      (required timing/availability fields, `confirm_latency_ms` STATIC), mirror the pin
      under `contracts/`, wire the CI conformance check. Command-surface input: the DES-1
      dossiers (`docs/devices/<slug>.md` §"Command surface"); slugs fixed 2026-07-12
      (owner): `revox-a77`, `revox-b215`, `pioneer-cld925`, `panasonic-fs90`.
      *(UNBLOCKED 2026-07-12 — repo-to-repo filing by the bridge session: convention v1 is
      designed, shipped, and TAGGED — pin ref `device-integration-v1` @ bridge `d273508`,
      artifacts `locveil-bridge/contracts/device-integration/` (guide +
      `device-descriptor.schema.json` + `STAMP.json`). Notables for this task: descriptors
      CARRY the canonical capability mapping (class-map dialect, `control` for `command`, no
      gate object — bridge derives it from the STATIC `timing.confirm_latency_ms`, required);
      names/labels ru+en required, de optional; `requires_arm` is a declared machine-readable
      interlock; availability = LWT `meta/online`; one retained `meta/locveil` stamp
      `{app, fw, descriptor, convention}` required. Canonical vocabulary must pre-exist
      bridge-side — the deck transport/record vocabulary does NOT yet; file the vocabulary
      request repo-to-repo when authoring (it lands with the bridge's EspManagedDevice work,
      golden catalog waits for the first deck config per HK-4).)*
      *(PROD-16 amendment 2026-07-12, filed with OPS-3: the convention pin lands as
      `contracts/pins/device-integration/` per `process/contracts.md` §2 — a COMPLETE
      artifact copy at the tag (guide + `device-descriptor.schema.json` + owner
      `STAMP.json` verbatim) + satellite `PIN.json` (files sha256s + conformance pointer
      to the descriptor CI check); the descriptors themselves are per-instance config
      validated AGAINST the pin, never pins. Intake wrinkle (recorded at OPS-3
      reconciliation): tag `device-integration-v1` (bridge `d273508`) carries the
      PRE-convention STAMP shape; the STAMP-core fix landed one commit later (bridge
      `eb08146`, VWB-41) with NO tag bump — since a pin is tag bytes, file the
      repo-to-repo request for a `device-integration-v1.1` minor tag when authoring
      (preferred), or pin at v1 and carry contract-guard's legacy warning until the next
      bump.)*

- [ ] **DES-5** [fleet] — **Device certificate lifecycle — revocation and renewal** (imported
      2026-07-12 from voice **ARCH-44**, export-closed there; travels with `provisioning/`).
      Plane B can *issue* device certs but never *withdraw* them: `esp32-provision revoke`
      only drops a **pending CSR**; once signed, a cert is trusted for its full **825 days**
      (`ssl_verify_client on`, no `ssl_crl`) — a lost/stolen/decommissioned satellite keeps
      firmware/model/`/ws/` access until expiry, and the only lever is re-issuing the whole
      CA. Symmetrically there is no renewal story (a batch provisioned together expires
      together). Design (before a real fleet exists): a CRL (`ssl_crl` + a `revoke-cert`
      verb regenerating it, nginx reload on change) or short-lived certs with auto-renew
      over mTLS; the operator verbs must distinguish *drop a pending CSR* from *revoke an
      issued cert*. Surfaced 2026-07-09 by voice's ARCH-25 provisioning round-trip.
      Deliverable: design doc + implementation follow-up(s). Refs: `provisioning/README.md`
      (Safety properties), `docs/design/esp32_satellite.md` D-17.
      *(PROD-24 expansion 2026-07-14 — board delegation, Workbench shell council; normative
      source `../locveil-commons/docs/design/workbench.md` §6. The design ABSORBS:
      **(a) the privileged broker** — one privileged code path, two peer clients (the
      `esp32-provision` CLI + the workbench provisioning page): a featherweight
      controller-side broker (key-owning user, localhost/unix-socket, authenticated zone)
      that both call. Owner overruled the CLI-only reading of D-17: the CLI's functionality
      MUST be replicated in the UI; the CA-key privilege boundary survives, the SSH-only
      gate does not — the **D-17 second amendment lands via this design**.
      **(b) the full verb vocabulary** — `list`/`status` (read surface; implies an
      `esp32-site` version bump), `approve`/`reject-pending` (broker v1; today's CLI
      `revoke` = drop-pending, reconciled at intake), `revoke-issued`/`renew` (this task's
      original core). **(c) the workstation operator-credential design** — client cert
      from the home CA vs a separate secret; the broker's authentication is this design's
      to define. Binding conditions on record: no write API ships before PROD-4's auth
      decision; the workbench page stays registry-declared dormant, gated on this task +
      first light; voice's desktop satellite is the page's first test target and needs the
      broker/read surface first. Deploy follow-through earmarked as **OPS-6**.)*

## PCB — board projects

_(none yet — opens after the governing DES designs; one `boards/<device>/` project per
device, tasks tagged `[dev:<board-slug>]`)_

## FW — firmware

_(gated on DES-3 — `phase-gates`)_

- [ ] **FW-1** [fleet] — **ESP32 satellite firmware build** (imported 2026-07-12
      from voice **ARCH-23**, export-closed there; reconcile at task start — the imported
      text predates HK-4). Build the headless voice-satellite firmware to the
      `docs/design/esp32_satellite.md` contract (D-1..D-18): board + digital I2S mic +
      MAX98357A speaker, half-duplex (D-2/D-7); the pinned voice wire protocol
      (`contracts/README.md` — register → PCM → end; reply channel
      `speak_begin`/PCM/`speak_end`); ported microWakeWord on `esp-tflite-micro` with the
      **TFLite-Micro micro-features frontend** + µVAD (D-9); models in a flash data
      partition, runtime-loaded (D-12) — the wake pack is voice's UNMODIFIED artifact,
      flash-time pinned, hash-verified (`consumer-pins`); two-stage SoftAP→STA provisioning
      + device admin UI + CSR submission against `provisioning/` (D-16/D-17);
      config-preserving OTA (D-18). **HK-4 amendments over the imported text:** per-device
      apps from shared `components/` (`per-device-apps` — no single image); the execution
      layer (PlatformIO vs alternatives, D-3) is **DES-3's decision, which gates this task**
      (`phase-gates`); rooms provisioning-time NVS. Also gated on hardware selection
      (PCB phase) — hence `HW-GATED`. Splits into per-device FW tasks (`[dev:<slug>]`) once
      the first board exists.
      *(DES-7 amendment 2026-07-17 — hardware ADOPTED: the voice satellite is the Waveshare
      ESP32-S3-Touch-LCD-1.46B `[dev:waveshare-lcd146]`, dossier
      `docs/devices/waveshare-lcd146.md` (full pin/strapping map for DES-3's audit), 3 units
      on hand — the hardware-selection gate lifts and the `HW-GATED` marker DROPS (bench
      hardware is on the desk; no PCB phase for this device). Read the imported text through
      the DES-7 amendments: "MAX98357A" = PCM5101A+NS8002 onboard (D-7 as amended); display
      support optional per the D-2 amendment (headless baseline; waveform listening animation
      nice-to-have; touch scope decided at THIS task's intake); µVAD compiles into the app
      image, models partition = wake pack only (D-9/D-12 as amended); power = USB-C only.
      Sole remaining gate: **DES-3**.)*

## DOC — documentation

- [ ] **DOC-2** — **Deck-corpus remediation from the DOC-1 audit**
      (`docs/review/doc1-deck-corpus-audit.md`; filed per `review-then-remediate`,
      owner ground rule: dossiers win). Fixes: **deck-common** — §1 power-rule exception
      pointer (F-1, FS90 §5.1 isolation-gate fallback), §2 reservoir topology reworded
      to the B215 bench-proven feed-series form (F-2), §2 idle-current figure corrected
      15 mA → the official ~2–4 mA ESP32 auto-light-sleep average, 15 mA kept only as
      declared sizing margin (F-5; the wrong figure is verbatim ESP8266 modem-sleep
      DTIM3 — provenance in the audit), §5 stale "legacy pin choices in the dossiers"
      referent reworded (F-6). **revox-b215** (additive only): 100–200 mA tap fuse into
      §3 (F-3), the common-§3 ground-vs-earth/chassis meter check into the §7 bench
      list (F-4). Optional hygiene: F-11 (trim B215's inlined reservoir values; hoist
      the default PC817 opto stage into common §4). Waveshare dossier untouched.

## OPS — operations / toolchain

- [ ] **OPS-1** — **Own the firmware publish pipeline into the WB7 `/srv/esp32/firmware/`.**
      The Plane-B nginx serves `/esp32/firmware/` from `/srv/esp32/firmware/`
      (operator-managed static); this repo owns how OTA images get published there
      (versioning, hashes). *(SPLIT 2026-07-14 at sprint-01 intake per `process/sprints.md`
      §4 — partial dependencies split the task: the model-pack half had zero dependencies
      and became **OPS-7** (the sprint-selected row — named "OPS-1a" there; renumbered at
      intake, scope-guard IDs are numeric-only — carrying the PROD-16 hash-at-publish
      amendment wholesale, it was always about the wake pack); this remainder is the
      firmware half, gated on the FW phase existing at all — no toolchain (DES-3), no
      images, nothing to publish. Reopens for real once FW-1 produces its first image.)*
- [ ] **OPS-6** [fleet] `EARMARK` — **Ansible-deploy rework for the DES-5 broker** (PROD-24
      delegation 2026-07-14; owner ruling: **not this sprint** — filed as an earmark, picked
      up only after DES-5 lands). `provisioning/ansible/deploy.yml` (Plane B) grows the
      broker deployment: the broker unit/service under its key-owning user, the
      localhost/unix-socket authenticated zone, operator-credential material, and whatever
      the DES-5 verb surface needs on the controller (e.g. CRL regeneration + nginx reload
      if DES-5 chooses `ssl_crl`). Blocked on DES-5 by definition — the design decides what
      gets deployed. Ref: `../locveil-commons/docs/design/workbench.md` §6.

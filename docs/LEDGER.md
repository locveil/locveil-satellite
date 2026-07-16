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
| `docs/review/des1-truth-pass.md` (2026-07-12) | DES-1 evidence: conflict resolutions, REQUIREMENTS disposition (VWB-38 feed), code sweep, pin re-audit |

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

- [ ] **DES-7** — **Voice-satellite hardware adoption: Waveshare ESP32-S3-Touch-LCD-1.46B**
      (owner decision 2026-07-16 — hardware selection is MADE: 3 units on hand, purchased
      2025; off-the-shelf board, no custom PCB for the voice satellite). Board ground truth
      (verified 2026-07-16 against the Waveshare wiki + official schematic + demo code):
      ESP32-S3R8, 8 MB octal PSRAM (D-2's floor exactly) + 16 MB W25Q128 flash; ONE I2S
      MEMS mic MSM261S4030H0R (ICS-43434-class — D-5 holds); PCM5101A I2S DAC + NS8002
      2.4 W amp + onboard speaker (functional substitute for D-7's MAX98357A; mic and DAC
      on separate I2S buses, so D-8's capture-16k / playback-22k05 coexistence holds);
      1.46" round 412×412 LCD + touch (SPD2010, QSPI); TCA9554 expander, QMI8658 IMU,
      PCF85063 RTC, microSD, ETA6098 Li-ion charge, USB-C; ~7 free GPIOs (none needed —
      all voice-satellite peripherals are onboard). Electronics identical across the
      1.46/1.46B/1.46C variants (B = no cover glass). Deliverables: **(a)** the
      voice-satellite device dossier `docs/devices/<slug>.md` (slug fixed at execution —
      DES-1 precedent) with the full pin/strapping map, feeding DES-3's mandatory audit;
      **(b)** `esp32_satellite.md` decision-log amendments — **D-2 amendment: display
      support becomes an OPTIONAL firmware feature** (compile-time flag per
      `per-device-apps`; the headless build stays the baseline); nice-to-have on top: a
      minimal "listening" animation while capture is active (owner 2026-07-16: the
      Siri-like *idea*, explicitly not Siri's UI) — **animation DECIDED 2026-07-16, owner
      picked variant B "waveform" of three mocked candidates**
      (`docs/design/assets/des7-listening-mockup.html` — open in a browser; A rings /
      B waveform / C rim-arc): five rounded vertical bars, center-weighted
      (0.55/0.82/1/0.82/0.55), heights driven by the speech envelope from the 16 kHz
      capture frames (per-bar phase wobble; the mockup's envelope is synthetic),
      cyan→violet vertical gradient #4FD8EB→#8B7BF7 on black; idle = the same bars as
      dim near-static dots (~35 % alpha); ~30 fps, five rounded rects — LVGL-cheap, no
      effects; D-7/D-8 notes (PCM5101A-for-MAX98357A;
      the board has NO AEC path — half-duplex v1 unchanged, and §14's v2 ES8311/AEC/2-mic
      upgrade is CLOSED on this hardware: v2 means new hardware); **D-9/D-12 clarifying
      amendment (owner 2026-07-16): the µVAD model is COMPILED INTO the app image** — the
      ESP32 analog of pymicro-vad's packaging (verified: the 2.0.1 wheel ships only the
      compiled extension, no `.tflite`); the models partition holds EXACTLY the wake pack
      (the unmodified HF artifact) — no fourth pin, no `publish_model_pack.py` extension;
      the VAD model is vendored third-party source with provenance recorded in the
      component README (upstream + version + sha256; candidates: `rhasspy/pymicro-vad`'s
      embedded model or `esphome/micro-wake-word-models` `vad.tflite` @ v2, ~16 KB tensor
      arena), and D-10's byte-identical device+server contract stays WAKE-model-only
      (server never runs VAD on the satellite path, D-11); one-time byte-diff vs the
      desktop wheel's model at FW build (end-hint parity check — same Ahrendt lineage,
      byte-identity unverified); **(c)** phase
      consequences recorded: no `boards/<slug>/` PCB project for the voice satellite, and
      FW-1's hardware-selection gate (the `HW-GATED` reason) lifts once this lands — FW
      still waits on DES-3 (`phase-gates`).

## PCB — board projects

_(none yet — opens after the governing DES designs; one `boards/<device>/` project per
device, tasks tagged `[dev:<board-slug>]`)_

## FW — firmware

_(gated on DES-3 — `phase-gates`)_

- [ ] **FW-1** [fleet] `HW-GATED` — **ESP32 satellite firmware build** (imported 2026-07-12
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

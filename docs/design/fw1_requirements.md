# FW-1 requirements record — ESP32 voice satellite (waveshare-lcd146)

Status: **AGREED 2026-07-20** (owner review, 3 rounds, artifact `d398d488` — the
council-style sheet with per-card verdicts; all 33 requirements approved, all 5 open
decisions closed). This record is the FW-1 intake baseline per
`task-start-reconciliation`: FW-1a/b/c (split per OPEN-5) execute against it. Sources
are the repo's normative docs — on any disagreement THOSE win: D-x =
`esp32_satellite.md`, E-x = `fw_execution_layer.md`, C-x = `satellite_enclosure.md`,
the `contracts/pins/` artifacts, `docs/devices/waveshare-lcd146.md`.

## A · Product scope

- **R-01 · The utterance loop.** Continuous capture → µVAD gate → wake → stream (with
  pre-roll) to `/ws/audio` → end-hint → the server's `{"type":"response"}` frame on the
  SAME socket is the utterance-complete ack → reply burst on `/ws/audio/reply` → play →
  re-arm. Safety nets: device 8 s cap, server 60 s force-finalize. *(pin §/ws/audio, D-6, D-8)*
- **R-02 · Pure voice terminal.** MQTT-unaware; NLU/actuation backend-side; reply
  channel carries SPEECH/TEXT only. *(D-4, D-1)*
- **R-03 · Display optional + extensible.** Compile-time flag; headless build = the
  definition of done. Display build compiles all three listening animations, per-unit
  NVS selection (default B "waveform"). The feature set is extensible post-v1 (backlog:
  tap-clock, timer countdown) without touching the headless baseline. *(D-2 as amended)*
- **R-04 · Unused peripherals stay unused.** IMU/RTC/SD/battery present-but-unused;
  USB-C only, no battery code. *(D-2/DES-7)*

## B · Platform & project shape

- **R-05 · IDF v6.0.2, native `idf.py`.** No PlatformIO, no Arduino;
  `esp-tflite-micro == 1.3.7` pinned with committed lock. *(E-1/E-2, FW-2 PASS)*
- **R-06 · Two identity layers.** Device-TYPE identity compile-time (one app per board
  type, boot asserts NVS matches image; multi-device image stays retired). Per-UNIT
  identity/config in NVS, written EXCLUSIVELY via the Stage-2 REST API from the
  workbench panel (+ build-time seed for first bring-up). *(per-device-apps, E-4, E-7)*
- **R-07 · Pin/strapping audit first.** E-6 gate — already discharged in the dossier §3;
  FW-1 consumes it as-is. *(E-6)*
- **R-08 · Flash layout.** OTA A/B app · NVS · wake-pack models partition; firmware /
  config / models separately versioned; config + models survive OTA; partition sized
  for pack growth. *(D-12, D-18)*

## C · Audio pipeline

- **R-09 · Lossless handovers + tunable wake-word cut.** ONE continuous I2S DMA capture
  into a ring buffer; VAD gates wake COMPUTE, not audio; streaming starts at
  trigger − offset from the same buffer. The offset is the wake-tail dial: set ≈ the
  model's measured detection latency (~100–300 ms) to cut the wake word while catching
  the utterance head; NVS-tunable, bench-calibrated; ~300 ms pre-roll capacity retained.
  Acceptance: sample-continuity check of a marked utterance at WB7. *(D-8, D-9)*
- **R-10 · Playback path built for real.** `speak_begin`/PCM/`speak_end` → I2S →
  PCM5101A/NS8002; declare `audio_out = {22050,1,16}` — the server converts to the
  declared format (pin guarantee; TTS-provider compatibility is voice's obligation, the
  satellite never resamples). Pair brackets by `seq`; jitter buffer; underrun = pad
  silence. The draft's output path was a stub — from-scratch build item. *(pin §reply, D-8)*
- **R-11 · Half-duplex, two I2S peripherals.** Capture-16k and playback-22k coexist; no
  barge-in; AEC/v2 closed on this hardware. *(D-7/D-8)*

## D · Wake word & VAD

- **R-12 · Exact micro-features frontend.** Wake models consume ~40-bin log-mel features
  (10 ms hop / ~30 ms window, PCAN) — the exact TFLite-Micro frontend `pymicro-features`
  wraps; anything else silently invalidates the pack's thresholds and breaks the
  device+server same-artifact guarantee. INT8 streaming inference via esp-tflite-micro;
  smoothed probability vs the manifest threshold. *(D-9/D-10; frontend choice per O-2)*
- **R-13 · µVAD compiled into the app image.** Vendored source + README provenance
  (upstream, version, sha256); build-time byte-diff parity check vs the desktop wheel.
  *(D-9/D-12 amendments)*
- **R-14 · End-of-utterance.** Emit `{"type":"end"}` on 700 ms trailing silence ∥ 8 s
  cap ∥ session end (all NVS-tunable); batch mode on the wire; server-streaming
  endpointing stays server-internal (ARCH-10). *(§4.4, D-6)*
- **R-15 · Wake pack sanctity.** Models partition = EXACTLY the pinned multi-model pack,
  hash-verified whole-pack, never modified; per-unit model selection at provisioning
  time via NVS/REST; pack version reported in `register`. *(consumer-pins, D-10/D-12)*

## E · Connectivity & wire protocol

- **R-16 · The ws-protocol pin is the contract.** Both WS surfaces per
  `contracts/pins/ws-protocol/websocket-api.md`; the doc wins; frame tables never
  duplicated repo-side. *(consumer-pins)*
- **R-17 · mTLS everywhere toward WB7.** Client cert on both WS + all HTTPS GETs; EC
  prime256v1; cert CN must equal `client_id`. *(D-17, pin CN rule)*
- **R-18 · Register & reconnect.** Register carries identity + `sample_rate: 16000` +
  `wants_audio: true` + `wants_trace: false` + `protocol_version` / `firmware_version` /
  `wake_pack_version` (registry stale-device tripwire; none gate registration). Ack
  gives `session_id` + server protocol version — mismatch = keep working, report loudly.
  Reconnect: per-socket exponential backoff + jitter (NVS-tunable bounds), re-register
  every connect; mid-utterance loss abandons the utterance cleanly; replies that fired
  while away are delivered at reply-reconnect and played. *(pin §register/§reply)*

## F · Identity, provisioning, lifecycle

- **R-19 · Per-unit data model.** NVS: `client_id` (= cert CN), `name`, `primary_room`,
  `covered_rooms[]`, wake-model ref, animation enum, tunables. Rooms are
  provisioning-time, picked from the catalog in the panel; voice registry authoritative;
  room semantics backend-owned. *(D-14/D-15)*
- **R-20 · Two-stage provisioning; Stage 2 REST-only.** Stage-1 SoftAP portal WITH its
  WiFi + WB7-address form in v1 (O-3); Stage-2 REST on `esp_http_server`, workbench page
  is the only UI; cert exchange never in AP mode; v1 no-auth (trusted LAN). *(D-16, E-4)*
- **R-21 · Born-stamped REST contract.** The change that first ships the API cuts
  STAMP + tag + registry row in the same change. *(HK-12/OPS-11)*
- **R-22 · CSR flow with pairing UX.** Device: keypair on-device (key never leaves), CSR
  to Plane-B `:8081`, poll/fetch signed cert. Approval surface = the workbench device
  page, Bluetooth-pairing-style (pending device + fingerprint → approve), driving the
  same Plane-B scripts; `esp32-provision` CLI remains the underlying layer/fallback.
  **Amends D-17** (recorded in `esp32_satellite.md`); the page itself is a cross-repo
  item filed when FW-1b starts. *(D-17 as re-amended)*
- **R-23 · OTA.** A/B `esp_https_ota` from Plane-B, pull-on-mismatch, validate,
  auto-rollback; NVS + models preserved. *(D-18)*
- **R-24 · Model push.** Ref = the pin tag (`wake-pack-vN`); bump = re-pin task +
  operator publish to `/srv/esp32/models/`; device checks at boot / register / REST
  trigger; staged download, whole-pack sha256, atomic swap, idle-state gate;
  reboot-free reload preferred, reboot acceptable v1; dev upload via REST. *(D-13)*

## G · Robustness & operational

- **R-25 · Session state machine.** idle → wake → capture/stream → await-response →
  playback → idle; half-duplex enforcement; WS/WiFi loss handled from any state;
  watchdog coverage. *(§3, D-4)*
- **R-26 · Bench workflow.** E-5 background build/flash/monitor pattern;
  `PATH="/usr/bin:$PATH"` before `export.sh`; BOOT/PWR pinholes are bench acts with no
  runtime function. *(E-5, C-9)*
- **R-27 · Tunables without reflash.** End-hint window, cut offset, thresholds, gain,
  timeouts — NVS-backed, REST-settable, for the DES-9 acoustic bench. *(D-8, E-4)*
- **R-28 · Dual-core split.** Core 0 = network/system (WiFi, lwIP, mbedTLS, WS, REST,
  OTA, state glue) + display (LVGL below network priority — frame drops invisible,
  starved audio is not); Core 1 = pinned audio real-time (I2S, features, wake, µVAD,
  playback feed), no network calls. Envelope-to-display via single-slot overwrite
  queue. Acceptance: zero capture overruns during concurrent TLS handshake + OTA
  download. *(owner NEW-1/r2)*
- **R-29 · C++.** All `locveil_*` components + app logic in modern C++ (GCC 15.2; exact
  `-std` recorded at project creation); C at IDF C-API boundaries and vendored C
  sources; IDF defaults on exceptions/RTTI stand. *(owner NEW-2)*
- **R-30 · Trace posture.** `wants_trace: false` in v1 (flippable via NVS/REST for bench
  debugging); the WS client tolerates-and-ignores optional/unknown text frames
  (`partial`, `trace`, future types). The satellite owes WB7 tracing nothing. *(pin §traces)*

## H · Interface summaries (approved surface lists)

- **R-31 · Offered REST API (v1 surface list; schemas at FW-1a/b).**
  `GET /api/v1/status` · `GET|PUT /api/v1/identity` · `GET /api/v1/wake/models` ·
  `PUT /api/v1/wake/model` · `PUT /api/v1/display/animation` ·
  `GET|PUT /api/v1/tunables` · `POST /api/v1/cert/csr` + `GET /api/v1/cert/status` ·
  `POST /api/v1/model/fetch` · `POST /api/v1/model/upload` (bench) ·
  `POST /api/v1/reboot`. Plain HTTP by design: the mTLS chain exists device→WB7 only;
  the workbench panel is HTTP on WB7 `:80` (same scheme, no mixed content); if the
  panel ever goes HTTPS its backend proxies device calls; device self-signed HTTPS
  stays the v2 option. Born-stamped at first ship (R-21). *(E-4 + review consolidation)*
- **R-32 · Consumed surfaces (closed list).** WSS `/ws/audio`, WSS `/ws/audio/reply`
  (ws-protocol-v1); HTTPS GET `/esp32/firmware/{ref}`, `/esp32/models/{ref}` (Plane B,
  mTLS); `:8081` bootstrap (CA GET, CSR PUT, cert GET — plain by design, human approval
  is the gate); mDNS advertise; SNTP only if/when the clock feature lands. Anything new
  comes back through review. *(pin, §12.4/12.5)*
- **R-33 · Timer cues.** Audible timer-done cue needs NOTHING in FW-1 — timers are
  backend-side and the reply channel already delivers announcements to the origin
  `client_id`; the cue itself is a voice feature. Countdown display is post-v1 (needs a
  new wire surface). **Filed: voice `ARCH-59`** (verify today's `timer.set` behavior —
  completion acknowledgement path + launch timestamp in the initiation ack). *(owner r2/r3)*

## Open-decision resolutions (O-1..O-5)

| # | Resolution (owner) |
|---|---|
| O-1 | Touch: present-but-unused in v1. Backlog concept: tap wakes display → digital clock for NVS-configurable seconds (SNTP time, RTC stays unused). |
| O-2 | Frontend: build BOTH (shipped signal-lib path + vendored legacy micro-features) behind one interface; the parity harness (feature tensors + wake scores vs desktop `pymicro-features`, on the pack's models) decides; loser is deleted; harness stays as the standing wake-stack test. |
| O-3 | Stage-1 WiFi form ships in v1 ("from day 1"). |
| O-4 | Bridge device-integration convention: NOT applicable to the satellite (voice-plane device, never bridge-actuated); pin deferred until a bridge-actuated device exists here — noted in `contracts/README.md`. |
| O-5 | FW-1 splits: **FW-1a** core loop to first light (audio + wake + both WS + state machine; NVS-seed provisioning; tunables slice of REST ships here WITH the API stamp) → **FW-1b** full provisioning + PKI pairing + OTA + model push (+ workbench-page cross-repo filing) → **FW-1c** display build. |

## Display-feature backlog (post-v1, compile-flag build only)

Tap-clock (O-1) · timer countdown (R-33, gated on voice ARCH-59 findings + a designed
event surface) · future animations join the R-31 animation config.

## Cross-repo queue from this review

- **voice `ARCH-59`** — FILED 2026-07-20 (timer-intent verification; R-33).
- **workbench device page: pairing UX + panel work** — file when FW-1b starts (R-22;
  relates voice ARCH-51 / board PROD-24 Workbench shell).
- **D-17 amendment** — recorded in `esp32_satellite.md` (this change).

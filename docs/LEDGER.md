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

- [ ] **OPS-1** — **Own the firmware/model publish pipeline into the WB7 `/srv/esp32/`.**
      The Plane-B nginx serves `/esp32/firmware/` + `/esp32/models/` from
      `/srv/esp32/{firmware,models}/` (operator-managed static); this repo owns how
      artifacts get published there (versioning, hashes, the wake-pack pin flow).

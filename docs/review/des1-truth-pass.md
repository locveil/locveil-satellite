# DES-1 — bridge ESP32 corpus harmonization: truth pass & merge record

**Date:** 2026-07-12. **Backs:** DES-1 (ledger). **Inputs:** the frozen import
`imports/bridge-esp32/` @ bridge `a80322f` (deleted in the DES-1 close — resolvable via
this repo's git history, import commit `0d950a9`): four per-device build docs
(`docs/wb-*.md`), the general research doc
(`docs/esp32-satellite-device-interface-research.md`), `REQUIREMENTS.md`, and the
driver sources. **Outputs:** `docs/devices/deck-common.md` + the four dossiers
(`revox-a77`, `revox-b215`, `pioneer-cld925`, `panasonic-fs90`).

**Method (HK-4 round 1, the DES-1 mandate):** claim-by-claim merge, never newest-wins.
The research doc is newer but WEAKER — it downgrades bench/manual-CONFIRMED facts to
VERIFY. Build docs are **leaf truth**; the research doc's cross-cutting engineering
rules survive where the build docs are silent.

---

## 1. Conflict resolutions (research doc vs build docs)

| # | Claim | Research doc said | Build doc says (leaf truth) | Resolution |
|---|---|---|---|---|
| 1 | B215 serial electrical layer | `[VERIFY] CRITICAL` — RS-232 vs TTL "decides the entire front-end"; populate-on-verify dual footprint | `[CONFIRMED]` SM §1.4: **neither** — bidirectional open-collector "Serie I/O" pin 3, opto-isolated, deck pull-up; ITT/Nokia pulse framing; device id 04 | Build doc wins; dual-footprint front-end idea RETIRED; MAX3232 never needed |
| 2 | B215 power | `[INFERRED]` internal 5 V rail, "verify location from SM + meter" | `[CONFIRMED]` +5 V on the SERIAL LINK DIN itself: pin 5, max 150 mA; pin 2 = floating GND reference | Build doc wins — no internal tap needed at all |
| 3 | A77 button emulation model | "close the relevant pin to the **switch common**" | `[CONFIRMED]` Fig. 7.1-86: each button closes a **pin PAIR** (floating SPST between two pins); REC = pin 6 fed via PLAY | Build doc wins; the "common rail" model was wrong and would have produced a wrong adapter |
| 4 | A77 pin→function map | `[VERIFY]` from SM fig 7.1-86 | `[CONFIRMED]` REW 8-9, FF 10-3, PLAY 4-5, STOP 1-2 (dummy pair), REC 6+PLAY, +27 V pin 7/150 mA, colours + centre "sw" | Build doc wins (it did the read the research doc asked for) |
| 5 | Pioneer control path | Option A SR jack (`[VERIFY]` waveform: "manual confirms the jack exists but not the protocol") vs Option B internal GP1U28X injection ("best-understood") | `[CONFIRMED]` external analysis: SR CONTROL IN = idle ~5 V, open-collector, ~100 kΩ pull-up, baseband IR copy, sleeve NOT grounded, RC-IX disables internal sensor | Build doc wins; **jack is primary**, internal injection demoted to documented fallback (its GP1U28X/CN301/PD3337A facts kept — they're manual-confirmed) |
| 6 | FS90 wired-control terminal | `[VERIFY]` "whether a rear edit/control terminal exists … may be cleaner than IR" | `[CONFIRMED]` none exists (SCART+IR only; edit ports were AG-series) — the build ADDS a Pioneer-style jack via parallel IR-OUT tap | Build doc wins; the added-jack design is the path |
| 7 | FS90 syscon | `[VERIFY]` IR module identity, output node, syscon input pin | `[CONFIRMED]` architecture (IR module → baseband → IC6001 MN153xx, 5 V logic via NV-VP60 SM); exact OUT pin deliberately bench-identified, not quoted | Build doc wins; the "don't trust a quoted pin for a solder point" rule is kept as stated |
| 8 | FS90 power-rail isolation | `[VERIFY] non-negotiable`: meter rail-gnd vs mains earth AND chassis before tapping; fallback paths if not isolated | Build doc only says "meter the rail under load" (headroom) — **under-weighted** | **Research doc wins this one** — the isolation check is a safety requirement the newer build doc dropped; reinstated as the FS90 dossier's gating bench item |
| 9 | Per-unit secondary-gnd vs earth checks (all decks) | present, per device | mostly absent | Kept from research doc in every dossier (deck-common §3) |
| 10 | Ground-domain rule, OTA-sizing tension, reservoir rationale, evidence-tag discipline | present (cross-cutting) | implicit only | Kept from research doc → `deck-common.md` §2–§3 |

Direction score: build docs won 7 of 8 direct conflicts — but #8 is the reminder of why
the merge is claim-by-claim and not newest-wins in *either* direction.

## 2. REQUIREMENTS.md truth pass (FR/NFR/C/EI disposition)

The imported spec described the retired single-image PIO firmware. Disposition of every
requirement, for the record and for bridge **VWB-38** (which promotes this FR-text into
wb-mqtt-v1):

| Req | Verdict | Where it lives now |
|---|---|---|
| FR-1 single image, FR-2 NVS runtime identity, FR-3 over-MQTT `/provision`, FR-4 closed identity set | **RETIRED** (HK-4; `per-device-apps`) | Compile-time identity + NVS assertion at boot; provisioning via `provisioning/` Plane B. The bridge-era MQTT ids (`revox_a77`, …) remain the likely wire-level ids — DES-4 decides |
| FR-5 announce (meta/name, meta/type, initial value, meta/online), FR-6 last-will, FR-7 subscribe `<c>/on` + FR-8 echo semantics | **TRUE, promotion material** — this IS the WB MQTT convention text VWB-38 formalizes as wb-mqtt-v1 | Bridge-owned convention; this repo consumes it via the `contracts/` pin (DES-4) |
| FR-9 DeviceDriver contract, FR-10 no core knowledge of devices | **SUPERSEDED** in mechanism, kept in spirit | The shared/per-device split is now shared `components/` + per-device apps |
| FR-11 per-device command surfaces | **TRUE, device truth** | Carried into each dossier's "Command surface" section (feeds DES-4 descriptors) |
| FR-12 record arming (8 s window, consumed on use) | **TRUE, convention** | `deck-common.md` §6 |
| FR-13 A77 reel-motion interlock (stop → wait ≤8 s → settle 500 ms) | **TRUE, device truth** | `revox-a77.md` §7 |
| FR-14 B215 never-drive-DATA-high, open-collector only | **TRUE, device truth (safety)** | `revox-b215.md` §2 |
| FR-15/16 Wi-Fi/MQTT connect-retry | **SUPERSEDED** — generic connectivity, now `locveil_wifi`/`locveil_wb_mqtt` component behaviour | Component design, FW phase |
| FR-17 OTA via MQTT-triggered HTTPS pull + rollback | **SUPERSEDED** as a flow; rollback + pull-not-push principles survive | `locveil_ota` against the WB7 `/esp32/firmware/` plane (OPS-1); design per `esp32_satellite.md` D-18 |
| NFR-1 light-sleep ≈15 mA, no manual `esp_light_sleep_start()` | **TRUE** | `deck-common.md` §2 |
| NFR-2 ≤1 s command latency | **TRUE, becomes descriptor timing data** | DES-4 (`confirm_latency_ms` is STATIC per HK-4) |
| NFR-3 PubSubClient ≥1024 B buffer | **RETIRED** (Arduino-era artifact; the import itself was already pure IDF `esp_mqtt_client`) | — |
| NFR-4 esp32dev / WROOM-32 target | **TRUE (deck family)** | `deck-common.md` §1. NB the voice satellite is ESP32-S3 class — different board, different dossier later |
| NFR-5 bit-bang in critical sections, RMT as fallback | **TRUE, technique note** | Dossiers (B215 §6, IR emit); revisit at FW phase |
| C-1 "PlatformIO + Arduino-ESP32" | **STALE EVEN AT IMPORT** — contradicted by the import's own CLAUDE.md (pure IDF since 2026-05-26, no Arduino). Execution layer is DES-3's decision | Recorded here as a corpus self-contradiction |
| C-2 PubSubClient | **RETIRED** (same Arduino-era artifact) | — |
| C-3 compile-time creds in config.h | **SUPERSEDED** | Provisioning design (SoftAP→STA + NVS; `esp32_satellite.md` D-16/D-17) |
| C-4 NVS namespace `bridge`/`device_id` | **SUPERSEDED** | `locveil_identity` design decides namespaces (FW phase) |
| C-5 wire protocol = WB topic convention, no abstraction | **TRUE in effect** | Formalized as wb-mqtt-v1 (VWB-38) instead of "no abstraction" |
| C-6 first flash USB, rest OTA | **TRUE** | `deck-common.md` §1 |
| C-7 GPIO34–39 input-only | **TRUE (chip fact)** | `deck-common.md` §5 |
| EI-2..EI-5 per-device electrical summaries | **TRUE** | Superseded in detail by the dossiers |

## 3. Code sweep (what the frozen source actually contained)

Verdict: **no unique bench truth in the code.** All protocol/timing tables are
placeholders (`T_START=0`, B215 frames `0x0000`, IR tables marked REPLACE with
shape-only NEC/Kaseikyo headers). The A77 GPIO map (STOP 14, PLAY 27, FF 26, REW 25,
REC 33, MOTION 34) and press/settle constants (200/400/500 ms) mirror the docs and are
themselves marked TODO-confirm — carried into the dossiers as `[INFERRED]` starting
points only. `LINK_INVERT=true`/`IR_INVERT=true` match the documented active-low
models. The one load-bearing find: **GPIO14 assigned in three drivers at once**
(`driver_a77.cpp:22`, `driver_b215.cpp:22`, `driver_ir.cpp:24`) — the concrete
double-booking behind HK-4's retirement of the single-image design; recorded in
`deck-common.md` §5.

## 4. ESP32 pin re-audit (against official Espressif documentation)

Checked 2026-07-12 via the Espressif docs MCP (ESP32 Series Datasheet §Boot
Configurations; ESP32 hardware-design-guidelines schematic checklist; ESP-IDF JTAG
tips-and-quirks):

- Strapping pins are **GPIO0, GPIO2, GPIO5, GPIO12 (MTDI), GPIO15 (MTDO)** — none of
  the legacy driver pins (14, 25, 26, 27, 33, 34, 35) is a strapping pin. ✔
- GPIO34–39 input-only: legacy use (34 motion, 35 status) is compliant. ✔
- **GPIO14 = MTMS (JTAG TMS)**, weak pull-up at reset — benign into a series-resistor
  opto LED; flagged in `deck-common.md` §5 for idle-low outputs and JTAG coexistence.
- Rule recorded for the PCB/FW phases: every per-device pin map is audited against the
  strapping/IO-MUX tables at design time (the mandatory DES-3 audit step).

## 5. Corpus disposition

- Four build docs + research doc + REQUIREMENTS → **absorbed** into
  `docs/devices/{deck-common,revox-a77,revox-b215,pioneer-cld925,panasonic-fs90}.md`;
  manual-scan images moved to `docs/devices/img/`.
- Trimmed as agreed (owner, 2026-07-12): Amazon.de shopping lists, "paste this file
  back" session prompts, bridge-repo path references (`cases/` STLs, `src/` layout).
  BOM essentials, safety rules, sources, bench checklists kept.
- `imports/bridge-esp32/` **deleted** in the DES-1 close (plain delete + journal
  pointer; content resolvable at import commit `0d950a9`).
- Repo-to-repo note filed to bridge **VWB-38**: the wb-mqtt-v1 promotion source is now
  §2 of this document + the dossiers' command surfaces, not the deleted
  `ESP32/REQUIREMENTS.md` copy.

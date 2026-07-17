# Firmware execution layer — the DES-3 decision (2026-07-17)

**Status:** AGREED 2026-07-17 (interactive owner session). Backs **DES-3**; unblocks the
FW phase (`phase-gates`). Evidence gathered same-day from the ESP Component Registry
(MCP), the espressif-docs MCP, and primary GitHub/PIO-registry sources; per-claim cites
inline. Companion inputs: `assets/des7-hardware-findings.md` §3 (vendor reference +
docs-MCP landscape), `../devices/waveshare-lcd146.md` (pin/strapping ground truth),
`esp32_satellite.md` (D-3/D-16 amended by this doc).

## E-1 — Execution layer = native `idf.py`. PlatformIO is OUT (D-3 amendment)

Owner decision, on this evidence:

- The 2024 Espressif/PlatformIO split froze the **Arduino** side only (official platform
  ships Arduino v2.0.17/IDF 4.4.7 forever); `framework=espidf` did keep moving —
  official `platform-espressif32` v7.0.0/v7.0.1 (2026-04/05) added IDF **6.0/6.0.1**.
  But: **no 6.0.2** (unpackaged 3+ weeks after IDF's release; PIO `framework-espidf`
  tops at 4.60001.0 = 6.0.1), a structural weeks-to-months lag behind every IDF release,
  and PlatformIO appears nowhere in Espressif's supported v6 tooling (native `idf.py`,
  EIM, VS Code extension). pioarduino: espidf only at 5.5.4, Arduino-centric,
  `prep_IDF6` branch unreleased.
- This repo gains nothing from PIO: `per-device-apps` maps 1:1 onto plain IDF app
  projects sharing `components/` (`EXTRA_COMPONENT_DIRS`); the vendor reference for the
  adopted board is itself a plain-`idf.py` project (findings §3.1); the espressif-docs
  MCP fact-checks the native workflow.

**Consequences:** D-3's "ESP-IDF + PlatformIO" is amended to **ESP-IDF + native
`idf.py`**; `no-execution-toolchain-at-bootstrap`'s PlatformIO question is closed
permanently (never install).

## E-2 — IDF target = v6.0.2, spike-gated; port-and-contribute is a sanctioned outcome

Owner posture (hardened 2026-07-17): strong preference for **v6.0.2** — aligns the
firmware with the latest-only docs MCP (findings §3.5).

- **The single v6-blocked dependency is `esp-tflite-micro`** (the D-9 wake stack): the
  registry constraint `idf >=5.0` admits 6.x, but its CI matrix ends at release-v5.5,
  and the Espressif maintainer confirmed (issue #125, 2026-04-06, still open at
  v1.3.7/2026-06-02): *"not updated to work with v6.0 … for now use release/v5.5"*,
  with v6 support promised. Whether the **core library** (we don't use the camera
  examples where the known breakage lives) compiles on 6.0.2 is **unverified**.
- **Decision:** install v6.0.2 (INFRA-1) and make the **first FW act a compat spike**:
  build the esp-tflite-micro core (a minimal micro-features + tiny-model harness) on
  6.0.2 for esp32s3.
  - Spike passes → pin the verified commit, report the datapoint upstream (#125),
    proceed on 6.0.2.
  - Spike fails → **port esp-tflite-micro to 6.0.2 ourselves and contribute upstream**
    (owner-sanctioned outcome, not a fallback trigger) — coordinating with #125 to
    avoid duplicating Espressif's in-flight work.
  - Bail-out (only if the port runs deep): **v5.5.4** — everything below is green on
    5.5.x, supported to ~Jan 2028; the machine's existing pristine-but-incomplete
    v5.5.0 tree (`~/esp/v5.5/esp-idf`) is the starting point, upgraded to 5.5.4.
- **Toolchain install = INFRA-1** (owner: separate task, new `INFRA` category):
  git clone at tag `v6.0.2` → `~/esp/v6.0.2/esp-idf` + `install.sh esp32s3`
  (matches the machine's `~/esp/<version>/` layout; pinnable checkout). The v5.5.0
  install stays untouched.

## E-3 — Dependency matrix vs IDF v6.0.2 (verified 2026-07-17)

| Component | Version | Declared IDF | v6.0 evidence | Role |
|---|---|---|---|---|
| `espressif/esp-tflite-micro` | 1.3.7 | >=5.0 | **BLOCKED** — CI ≤5.5, maintainer-confirmed (#125); spike per E-2 | D-9 wake stack |
| `espressif/esp_websocket_client` | 1.7.0 | >=5.0 | CI updated for IDF v6.0 (1.6.0 changelog); mTLS supported | voice WS wire (`consumer-pins`) |
| `espressif/mdns` | 1.11.3 | >=5.0 | same esp-protocols repo/CI family | D-16 `<host>.local` |
| `espressif/esp_lcd_spd2010` | 2.0.0 | >=5.3 | **explicit**: "Compatible with ESP-IDF v6.0" (changelog 2025-10-29) | display (optional feature) |
| `espressif/esp_lcd_touch_spd2010` (+ `esp_lcd_touch` 1.2.1) | 2.0.1 | >=5.3 | maintained 2026-04 | touch (present-but-unused v1) |
| `espressif/esp_io_expander_tca9554` | 2.0.3 | >=5.2 | already on the new `i2c_master` API | LCD/touch resets |
| `espressif/esp_lvgl_port` + `lvgl/lvgl` | 2.8.0 / **pin ^9** | >=5.2 | explicit IDF6 fixes in 2.6.1/2.7.1 | animation rendering |
| `espressif/cjson` (or idf-extra) | registry | — | cJSON **moved out of IDF in 6.0** — take as managed dependency | WS control frames, REST bodies |

Core-IDF surface (versioned with the IDF): `i2s_std` (both audio paths; the legacy I2S
driver v6 removed is NOT what we use), `esp_http_server` (E-4), `esp_https_ota`, NVS,
`esp_wifi`/`esp_netif`, LEDC (backlight), mbedTLS.

**v6.0 migration notes that touch us** (migration guide + release notes, verified):
legacy ADC/DAC/I2S/timer drivers removed (we're on new APIs); legacy I2C is EOL-not-
removed until v7 (affects only vendor-demo *reading*); **default warnings are errors**
(mind the vendored µVAD source, D-9); `wifi_provisioning` left the IDF (irrelevant —
D-16 rolls its own portal on `esp_wifi` + `esp_http_server`); mbedTLS 4.x/PSA adds
~30–40 KB flash and phases legacy crypto APIs — **FW-1 check item: the D-17 on-device
CSR-generation path (mbedtls x509write_csr) against PSA-era mbedTLS**.

## E-4 — Device REST API on core `esp_http_server`; D-16 Stage-2 goes REST-only

- The firmware's management surface is a **REST API served by core `esp_http_server`**
  (no external framework — cJSON for bodies is the only dependency). Surface (v1
  sketch, finalized at FW-1): identity (`client_id`, name, room), wake-model selection
  (from the pack manifest), listening-animation variant, audio tunables (end-hint
  window), CSR/cert lifecycle triggers, status (versions incl. pack version, health).
- **D-16 amendment (owner 2026-07-17): Stage 2 has NO on-device HTML** — all
  configuration UI lives in the **workbench-hosted management page** driving this API.
  **Stage 1 (SoftAP captive portal + minimal WiFi form, the mitsubishi2wb
  first-boot-hotspot pattern) stays device-hosted** — it runs before the device has a
  network. Owner note: the Stage-1 form itself **may slip past v1** — the sanctioned
  build-time NVS seed (`per-device-apps`) covers first provisioning of the three
  on-desk units; the portal remains the design for any unit beyond arm's reach.

## E-5 — Agent-session build/flash/monitor pattern (the "background monitor")

`idf.py` workflows in Claude sessions run as **background Bash tasks**: long steps
(`idf.py build`, `flash`, `monitor`) launch with `run_in_background`, the session
continues, and completion re-invokes the agent; `idf.py monitor` output is captured to
the task log and read incrementally (never blocking the session on an interactive
monitor). Flash/monitor need the physical device on USB — those steps are inherently
bench-side; build/size/static checks are not.

## E-6 — The mandatory pin/strapping audit step (defined)

Every per-device FW app passes this gate **before its first flash** (the GPIO14
lesson; `phase-gates`):

1. The app's pin map is written against the device dossier (`docs/devices/<slug>.md`),
   never against sample code.
2. Each used GPIO is checked against the chip's strapping/IO-MUX restriction tables
   (datasheet §Boot Configurations + TRM IO_MUX list, via the docs MCP) — strap
   conflicts, input-only pins, flash/PSRAM-reserved pins.
3. The audit result is recorded in the dossier (or its update) with sources.

For the voice satellite this step is **already discharged**: `waveshare-lcd146.md` §3
(GPIO45/46-on-LCD assessment, octal-PSRAM pin claims, USB-JTAG pins) — FW-1 consumes
it as-is.

## E-7 — Project shape (records the layout the invariants imply)

- One IDF project per device app under the FW tree; shared code as IDF components in
  `components/` (`locveil_wifi`, `locveil_wb_mqtt`, `locveil_ota`, `locveil_identity`,
  `locveil_ir_baseband`, + the audio/wake components FW-1 defines), consumed via
  `EXTRA_COMPONENT_DIRS`. Registry deps pinned per-app in `idf_component.yml`.
- Display-enabled voice-satellite build = the same app with the compile-time display
  feature (D-2 as amended); LVGL pinned `^9`.
- The Waveshare demo stays a reading reference only (unlicensed — findings §3.1); the
  factory `.bin` is the bench restore.

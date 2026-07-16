# DES-7 findings — Waveshare ESP32-S3-Touch-LCD-1.46B: enclosure data + vendor software survey

> Input evidence for **DES-7** (voice-satellite hardware adoption). Gathered 2026-07-16 in an
> interactive owner session; every claim below was verified against the named source on that
> date, not recalled from memory. Companion asset: `des7-listening-mockup.html` (the three
> listening-animation candidates; owner picked variant B — see the DES-7 ledger entry).

## 1. Scope and sources

- Owner hardware on hand: **3× ESP32-S3-Touch-LCD-1.46B** (purchased 2025).
- Sources: Waveshare wiki (`https://docs.waveshare.com/ESP32-S3-Touch-LCD-1.46`), the
  wiki's Resources page, the vendor's structural-diagram archive (contents inspected),
  the official schematic PDF, `github.com/waveshareteam` (org + board repo trees read via
  the GitHub API), and the ESP Component Registry (queried via MCP).
- Variant note: **1.46 / 1.46B / 1.46C electronics are identical**; B = no cover glass,
  C = widened cover glass. All mechanical data below is for the B (no-cover) variant
  unless stated.

## 2. Enclosure / mechanical — verdict: everything CAD needs exists

The wiki page itself undersells the mechanical data; the substance is inside the
"Structural Diagram" RAR archives on the Resources page.

### 2.1 File inventory (vendor-hosted; hashes pin the 2026-07-16 downloads)

| File | What it is | sha256 |
|---|---|---|
| `ESP32-S3-Touch-LCD-1.46B_Structural Diagram-Without Cover.rar` (2.3 MB) | archive holding both files below; URL: `https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-1.46/ESP32-S3-Touch-LCD-1.46B_Structural%20Diagram-Without%20Cover.rar` | `4647210e9f1a88e4e7f1fb6ab277fdcd32d86f6f76424208cb7cee0cfe2e8220` |
| `ESP32-S3-LCD-1.46.pdf` (119 KB) | dimensioned 2D mechanical print, 3 views | `ff0da26715dd5ecb2869116524ffa4b5328de4aeb68cfd181eb14d6369a42c8c` |
| `ESP32-S3-LCD-1_46.stp` (14.8 MB) | full 3D STEP assembly (Creo Parametric export, dated 2024-10-14, 219 components) | `0587a0963343f610a35d719633cd7912532fa5e1d424c63be8f774b289eb92b3` |

A sibling "With Cover" archive exists for the glass variant (not needed for the B).
The files are NOT committed here (14.8 MB STEP); re-download and verify against the
hashes, or re-pull the RAR before enclosure CAD starts.

### 2.2 The 2D print (dimensions that matter for the case)

- Board outline **39.36 ±0.1 × 41.53 ±0.1 mm**; back-view width across the mounting
  bosses 39.18 mm.
- Thickness stack: **9.0 mm total**; 5.5 mm from PCB to the display face;
  LCM (display cell) **1.51 ±0.1 mm**.
- Display: **36.96 mm active area**, **37.36 ±0.15 mm viewing area** — with no cover
  glass on the B, these two circles decide what a printed bezel lip may cover (nothing
  inside 37.36) and where it must sit to protect the bare panel edge.
- Mounting: **3× M2.0 threaded bosses, 3.5 mm thread depth** (`3*M2.00-H3.5`), positions
  fully dimensioned on the back view (verticals 19.64 / 17.75 / 14.95 / 23.00 mm,
  horizontals 12.00 / 11.54 mm, boss-circle width 39.18 mm, 15.45 mm datum) — the board
  screws in, no clips needed. Screw length budget = wall + 3.5 mm max engagement.
- USB-C position at the bottom edge is dimensioned.

### 2.3 The STEP assembly (the real prize)

Full PCBA, 219 modeled components — every case aperture can be cut against actual
geometry instead of calipers. Confirmed present by product name in the STEP:

- `MIC` (the MEMS microphone body),
- `SPK-12-10-2_8MM` — the speaker, **12 × 10 × 2.8 mm** (orientation/radiating face:
  read from the STEP while modeling),
- `TYPE-C_16PIN-9X3X7_3` (USB-C shell), `SWITCH-TS24CA` (both side switches),
- `MICRO_SD_SOCKET_PU`, `1_27MM-2X10PIN` header, antenna, battery connector.

### 2.4 Acoustics — the D-7 "dominant quality lever"

- The mic (**MSM261S4030H0R**, MEMSensing) is **top-ported** — confirmed from the
  datasheet Waveshare itself hosts, cross-confirmed via SnapEDA and DFRobot copies.
  The sound inlet is on the mic's body facing outward, NOT through the PCB. Case
  consequence: a short **gasket-sealed channel** aligned over the mic body (hole in the
  case wall + compliant ring sealing the path); no through-PCB port complications.
- Speaker: no frequency-response or porting data is published for the 12×10×2.8 mm
  speaker. Case wants a grille and ideally a small sealed back volume; final tuning is
  a bench matter.

### 2.5 Not in the vendor data (none of it blocks CAD)

1. **Antenna keep-out** — position is in the STEP but no guidance published; standard
   practice applies (plastic only near the antenna, no metal fasteners adjacent).
2. **Owner decisions, not missing info**: battery cell dimensions (MX1.25 2-pin pocket),
   device posture (desk puck vs wall — decides mic-channel and speaker-outlet
   direction), bezel-lip protection for the glass-less panel.

## 3. Vendor software survey — `github.com/waveshareteam` (100+ repos)

### 3.1 `ESP32-S3-Touch-LCD-1.46` — the board's own repo (the important one)

- Contains, beyond the Arduino demo, a **complete native ESP-IDF 5.3.2 project**
  (`example/ESP-IDF-5.3.2/ESP32-S3-Touch-LCD-1.46-Test/`) with per-peripheral drivers:
  SPD2010 display (own `esp_lcd_spd2010` port) + SPD2010 touch, `PCM5101.c` playback,
  `MIC_Speech.c` capture, **TCA9554PWR expander** (gates LCD/touch reset — a bring-up
  landmine worth knowing in advance), PCF85063 RTC, QMI8658 IMU, SD_MMC, battery ADC,
  power-latch key, LVGL glue.
- **Wiring truths that cost bench days**, read from the source: the mic capture runs
  **32-bit I2S slots with the RIGHT slot mask** at 16 kHz (`MIC_Speech.c`,
  `I2S_STD_SLOT_RIGHT`, 32-bit width) — invisible in the schematic.
- **Voice pipeline proven on this hardware**: the demo runs Espressif esp-sr WakeNet
  (~1.9.4) from the onboard mic. We use microWakeWord instead (D-9), but
  mic → AFE → wake working on this exact board removes the "does audio even work" risk
  class. Also a **DES-3 datapoint**: the vendor's own reference is plain `idf.py` on
  **IDF 5.3.2** — validates the native-IDF option; known-good IDF version anchor.
- Factory demo image `Firmware/ESP32-S3-Touch-LCD-1.46.bin` — bench sanity-restore.
- Demo deps pin **LVGL ~8.3** (not 9). The decided variant-B listening animation is
  procedural (five rounded rects) and renders on either; only the (unused) Lottie route
  would force LVGL 9. Do not inherit their LVGL pin blindly.
- **License caveat: the repo has NO license file** (GitHub license API 404s). Verbatim
  vendoring of Waveshare driver code is therefore murky; the consumption model below
  avoids it.

### 3.2 ESP Component Registry — maintained drivers cover the hard parts

Verified in the registry (2026-07-16): **`espressif/esp_lcd_spd2010`** (SPI & QSPI) and
**`espressif/esp_lcd_touch_spd2010`** are official Espressif-maintained components.
Realistic consumption model for FW-1:

> registry components for display/touch (and likely the TCA9554 expander) + our own
> thin I2S/driver glue + Waveshare's demo used as a *reading reference* for pin maps,
> slot masks, and init order — no verbatim vendoring of unlicensed code.

### 3.3 `Waveshare-ESP32-components` — BSP watch

Waveshare publishes ESP-IDF BSPs to the component registry (~23 boards, CI-checked).
**No BSP for the 1.46 exists yet.** Worth a periodic glance: if
`esp32_s3_touch_lcd_1_46` appears, board bring-up collapses to one
`idf.py add-dependency`.

### 3.4 Marginal

- `ESP32-AIChats` — pointer collection (xiaozhi-esp32, doubao, openai-RTC) for
  cloud-LLM voice chat; wrong architecture for us (own backend + pinned WS protocol),
  but xiaozhi is a mature S3 voice-assistant firmware for UX comparison if ever wanted.
- `1.46inch-Touch-LCD-Module` — bare panel module repo, redundant given §3.1.

## 4. Consequences by ledger task

- **DES-7** — this doc is dossier input: §2 feeds the enclosure part of the dossier,
  §3.1's pin/slot truths feed the pin/strapping map, §2.4 discharges the "which side is
  the mic ported" question for the D-7 acoustic amendment.
- **DES-3** — §3.1: vendor reference on native IDF 5.3.2 validates the `idf.py` option;
  demo's esp-sr proof + LVGL 8.3 pin are version-alignment datapoints.
- **FW-1** — §3.2's consumption model (registry drivers + own glue, no unlicensed
  vendoring); the 32-bit/RIGHT-slot mic config; the factory `.bin` as bench restore.

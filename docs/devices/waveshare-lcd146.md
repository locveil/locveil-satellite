# Waveshare ESP32-S3-Touch-LCD-1.46B — device dossier `[dev:waveshare-lcd146]`

The **voice satellite** (design: `../design/esp32_satellite.md`, adopted by **DES-7**,
owner decision 2026-07-16). Off-the-shelf board — **no `boards/<slug>/` PCB project**;
3 units on hand (purchased 2025). Input evidence + enclosure data:
[`../design/assets/des7-hardware-findings.md`](../design/assets/des7-hardware-findings.md).

**Status.** Pin map, strapping audit, and peripheral inventory `[CONFIRMED]` from the
official schematic PDF + the vendor's ESP-IDF demo sources + the Waveshare wiki,
cross-checked claim-by-claim (all three sources agree on every pin; divergences noted
inline). Chip-level strap/PSRAM truths `[CONFIRMED]` against the ESP32-S3 datasheet/TRM
via the Espressif docs MCP (2026-07-17). Open bench items in §9 — the board boots the
factory image, so nothing below is first-light-blocking.

**Sources pinned:** demo code `github.com/waveshareteam/ESP32-S3-Touch-LCD-1.46` @ `main`
= **`fda89ff2ff32eb1bce561901225c6a36fa684237`** (2026-04-30); official schematic
`https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-1.46/ESP32-S3-Touch-LCD-1.46.pdf`
(p.1 carries a full GPIO-usage matrix); wiki page **`ESP32-S3-Touch-LCD-1.46B`** (the
plain-1.46 wiki URL is a stub; the B page self-identifies as the 1.46 — electronics are
identical across 1.46/1.46B/1.46C, B = no cover glass). Code paths below are relative to
`example/ESP-IDF-5.3.2/ESP32-S3-Touch-LCD-1.46-Test/main/`. The demo code is
**UNLICENSED — reading reference only, never vendored** (findings §3.1/§3.2).

---

## 1. Identity & role

- **SoC:** ESP32-S3R8 — 8 MB **octal** PSRAM in-package (D-2's floor exactly) +
  16 MB W25Q128 QSPI flash. Flash budget: OTA A/B app + NVS + models partition (the
  models partition holds the **whole multi-model wake pack** — one wake model per unit,
  ≥3 near-term; D-12 as amended).
- **Role config (owner, 2026-07-16/17):** power **USB-C only** (Li-ion path unused, no
  cell); enclosure posture **wall-mounted**; display support **optional** firmware
  feature (headless baseline, D-2 as amended); touch/IMU/RTC/SD present-but-unused
  (touch scope decided at FW-1 intake).
- All voice-satellite peripherals are onboard — the free GPIOs (§8) are spare, nothing
  external is required.

## 2. Pin map `[CONFIRMED]` (sch p.1 GPIO matrix + demo headers + wiki tables)

| GPIO | Board function | Net | Source |
|---|---|---|---|
| 0 | **BOOT button** (Key2 → GND, 10 K pull-up R28); also on header | `IO0` | sch p.1; strap §3 |
| 1 | free (header) | `GPIO1` | sch p.1 |
| 2 | **I2S mic WS** | `MIC_WS` | `MIC_Driver/MIC_Speech.h:15`; wiki; sch |
| 3 | free (header) | `GPIO3` | sch p.1; strap §3 |
| 4 | touch INT — wired, demo polls instead (never configured) | `TP_INT` | `Touch_Driver/Touch_SPD2010.h:7`; sch |
| 5 | **LCD backlight PWM** (LEDC ch0, active-high → Q3 FET → LEDK) | `LCD_BL` | `LCD_Driver/Display_SPD2010.h:45`, `.c:123-144` |
| 6 | **PWR button** input (Key1, active-low) | `Key_BAT` | `PWR_Key/PWR_Key.h:4`; sch |
| 7 | **power-latch** output (8050 T1 → AO3401 Q1; high = battery rail held) | `BAT_Control` | `PWR_Key/PWR_Key.h:5`; sch |
| 8 | battery ADC, ADC1_CH7 (200 K/100 K divider; ×3 + 0.990476 offset in code) — **unused, no cell** | `BAT_ADC` | `BAT_Driver/BAT_Driver.h:13`, `.c:81-93`; sch |
| 9 | RTC interrupt — wired, unused by demo | `RTC_INT` | wiki; sch |
| 10 | **I2C SCL** — shared bus: SPD2010-touch 0x53, TCA9554 0x20, PCF85063 0x51, QMI8658 (§7) | `SCL` | `I2C_Driver/I2C_Driver.h:11`; wiki; sch |
| 11 | **I2C SDA** (same bus) | `SDA` | `I2C_Driver/I2C_Driver.h:12` |
| 12 | free (1.27 mm header) | `GPIO12` | sch p.1 |
| 13 | free (1.27 mm header) | `GPIO13` | sch p.1 |
| 14 | SDMMC CLK (1-bit) — SD unused in role | `SD_SCLK` | `SD_Card/SD_MMC.h:16`, `.c:79-86` |
| 15 | **I2S mic BCLK** | `MIC_SCK` | `MIC_Driver/MIC_Speech.h:14` |
| 16 | SDMMC D0 | `SD_MISO` | `SD_Card/SD_MMC.h:18` |
| 17 | SDMMC CMD | `SD_MOSI` | `SD_Card/SD_MMC.h:17` |
| 18 | LCD tearing-effect — wired, never configured by demo | `LCD_TE` | `LCD_Driver/Display_SPD2010.h:37` |
| 19 | USB D− | `D_N` | wiki; sch |
| 20 | USB D+ | `D_P` | wiki; sch |
| 21 | **LCD QSPI CS** | `LCD_CS` | `Display_SPD2010.h:43`, `.c:59` |
| 26–32 | in-package flash — never usable | — | S3 datasheet §2.3.4 |
| 33–37 | octal PSRAM ("Internal occupancy") — never usable on S3R8 | — | sch p.1; S3 datasheet/IDF GPIO table |
| 38 | **I2S DAC LRCK** (PCM5101A) | `I2S_LRCK` | `Audio_Driver/PCM5101.h:17` |
| 39 | **I2S mic DIN** | `MIC_SD` | `MIC_Speech.h:17` |
| 40 | **LCD QSPI SCK** | `LCD_SCK` | `Display_SPD2010.h:38` |
| 41 | LCD QSPI DATA3 | `LCD_SDA3` | `Display_SPD2010.h:42` |
| 42 | LCD QSPI DATA2 | `LCD_SDA2` | `Display_SPD2010.h:41` |
| 43 | UART0 TXD (header) | `UART_TXD` | wiki; sch |
| 44 | UART0 RXD (header) | `UART_RXD` | wiki; sch |
| 45 | LCD QSPI DATA1 — **strapping pin, see §3** | `LCD_SDA1` | `Display_SPD2010.h:40`; sch |
| 46 | LCD QSPI DATA0 — **strapping pin, see §3** | `LCD_SDA0` | `Display_SPD2010.h:39`; sch |
| 47 | **I2S DAC DIN** (PCM5101A) | `I2S_DIN` | `PCM5101.h:18` |
| 48 | **I2S DAC BCLK** | `I2S_BCK` | `PCM5101.h:15` |

### TCA9554 I2C expander (addr **0x20**; code's `EXIOn` = chip pin P(n−1); demo sets all
pins output at init, `EXIO/TCA9554PWR.c:90-94`)

| EXIO | Function | Source |
|---|---|---|
| EXIO1 (P0) | **touch reset** `TP_RST` (pulse low ~50 ms) | `Touch_SPD2010.c:34-36`; sch |
| EXIO2 (P1) | **LCD reset** `LCD_RST` (pulse low) | `Display_SPD2010.c:8-10`; sch |
| EXIO3 (P2) | SD DAT3/CS — never driven by demo; SDMMC 1-bit mode relies on the power-on default | wiki; sch |
| EXIO4 (P3) | IMU INT2 (unused) | wiki; sch |
| EXIO5 (P4) | IMU INT1 (unused) | wiki; sch |
| EXIO6–8 | unconnected | sch p.1 |

**Bring-up landmine (findings §3.1):** LCD and touch resets are **behind the expander** —
no I2C + TCA9554 init, no display/touch, even with perfect QSPI wiring.

**Stale-define warning:** demo `SD_Card/SD_MMC.h:23` has `CONFIG_SD_Card_D3 21` —
**wrong** (GPIO21 is LCD_CS); it is referenced nowhere and `slot_config.d3 = -1`. The
real SD DAT3 is EXIO3. Never copy that define.

## 3. Strapping audit `[CONFIRMED]` (DES-3 mandatory-audit input; chip truth: ESP32-S3 datasheet §Boot Configurations + TRM ch.8)

ESP32-S3 straps: **GPIO0 + GPIO46** = boot mode, **GPIO45** = VDD_SPI voltage,
**GPIO46** also ROM-log print, **GPIO3** = JTAG source. Defaults: GPIO0 weak pull-up (1),
GPIO3 floating, GPIO45/46 weak pull-down (0).

| Strap | Board use | Verdict |
|---|---|---|
| GPIO0 | BOOT button + 10 K pull-up to 3V3 | textbook — hold at reset for download mode |
| GPIO3 | nothing on-board (free header pin) | floating strap, safe; leave unloaded at reset if ever used |
| GPIO45 | **LCD QSPI DATA1** | shared with a display data line — see below |
| GPIO46 | **LCD QSPI DATA0** | shared with a display data line — see below |

**GPIO45/46-on-LCD assessment.** Vendor-designed-in and empirically fine (three units +
factory image boot normally): at power-on the TCA9554 holds LCD_RST high-Z (its pins
power up as inputs) and the un-initialized SPD2010 does not drive its QSPI data lines,
so the chip's weak pull-downs win and both straps read their defaults (GPIO45=0 →
VDD_SPI 3.3 V, correct for the W25Q128; GPIO46=0 → ROM log on). Two cautions carried
forward:

1. **Download mode**: entering it needs GPIO0=0 **and GPIO46=0** at reset (GPIO0=0 with
   GPIO46=1 is the documented invalid combination). If flashing is ever flaky on a unit
   with firmware that has initialized the display, suspect SPD2010 activity on
   `LCD_SDA0`/GPIO46 during the reset — power-cycle (not just EN-reset) before BOOT.
   `[VERIFY]` on bench once (§9).
2. Firmware must never repurpose GPIO45/46 for anything but the LCD QSPI signals the
   board wires them to.

No other strap conflicts exist — this board passes the GPIO14-lesson audit (GPIO14 is
plain SDMMC CLK here; MTMS/JTAG pins GPIO39–42 carry mic-DIN/LCD-QSPI, irrelevant since
debugging runs over USB-Serial-JTAG on GPIO19/20).

## 4. Audio `[CONFIRMED]`

- **Mic — MSM261S4030H0R** (MEMSensing, I2S digital MEMS, ICS-43434-class → D-5 holds),
  **top-ported** (datasheet Waveshare hosts + SnapEDA/DFRobot cross-check; findings
  §2.4): case gets a gasket-sealed channel over the mic body, no through-PCB port.
  Pins: BCLK 15 / WS 2 / DIN 39. **Wiring truth invisible in the schematic:** capture
  runs **32-bit std slots with `I2S_STD_SLOT_RIGHT`** at 16 kHz (`MIC_Speech.c:33-35`) —
  hardware-fixed by L/R strapped to 3V3 (R27 0R) and EN to 3V3 (R26 0R, always on; no
  mic-enable GPIO).
- **Playback — PCM5101A I2S DAC + NS8002 2.4 W amp + onboard speaker** (functional
  MAX98357A substitute, D-7 as amended). Pins: BCLK 48 / LRCK 38 / DIN 47; **no MCLK**
  (`PCM5101.h:16`). **No amp-enable GPIO** — NS8002 shutdown pin is hardwired active,
  volume is the physical 10 K trimmer R57. Nothing to mute in firmware except zeroing
  the stream.
- **Port assignment:** mic and DAC sit on **disjoint pin sets**, so peripheral
  assignment is a firmware-only choice. The vendor demo routes audio through
  `I2S_NUM_0` (`PCM5101.h:12`) — a same-rate convenience read. Our D-8 dual-rate
  topology (capture 16 k / playback 22.05 k coexisting) assigns the S3's **two
  independent I2S peripherals** (e.g. I2S0 capture, I2S1 playback).
- **No AEC path** anywhere on the board — half-duplex v1 stands; §14 v2 audio upgrades
  are closed on this hardware (v2 = new hardware).

## 5. Display & touch `[CONFIRMED]` (optional feature, D-2 as amended)

- **SPD2010** 1.46" round 412×412 LCD + capacitive touch, one chip. QSPI: SCK 40,
  DATA0–3 = 46/45/42/41, CS 21, TE 18 (unused); backlight PWM GPIO5 (LEDC); resets on
  EXIO1/EXIO2 (§2). Touch on the shared I2C at 0x53, INT GPIO4 (demo polls).
- Consumption model (findings §3.2): **espressif/esp_lcd_spd2010 + esp_lcd_touch_spd2010**
  registry components + own glue; demo pins LVGL ~8.3 — the decided waveform animation
  (five rounded rects) renders on LVGL 8 or 9, do not inherit the vendor pin blindly.
- Headless baseline: backlight held off (GPIO5 low) and display/touch left in reset is a
  valid do-nothing state — both resets sit behind the expander.

## 6. Power `[CONFIRMED]` — role: USB-C only

- USB-C (D− 19 / D+ 20; also flash/debug via USB-Serial-JTAG), ETA6098 Li-ion charger +
  MX1.25 battery connector + battery ADC GPIO8 — **all unused in role** (no cell).
- **Power latch exists regardless:** Key1 (GPIO6) + `BAT_Control` (GPIO7) drive a
  battery-rail latch (8050 → AO3401). On USB power the 5 V→3V3 path supplies the board
  without the latch. `[VERIFY]` §9: confirm a USB-only unit boots with no PWR-key press
  and that firmware can ignore GPIO6/7 entirely (expected — the factory image runs on
  USB-only bench setups).
- Enclosure consequence: no battery pocket (findings §2.5 item resolved).

## 7. Present-but-unused peripherals `[CONFIRMED]`

- **PCF85063 RTC** (I2C 0x51, INT GPIO9): irrelevant — server-authoritative time.
- **QMI8658 IMU** (shared I2C; INT1/INT2 on EXIO5/EXIO4): unused. I2C address strap
  0x6B vs 0x6A `[VERIFY]`-if-ever-used (demo header defines both).
- **microSD** (SDMMC 1-bit: CLK 14, CMD 17, D0 16, DAT3/CS EXIO3): unused; models live
  in flash (D-12).

## 8. Free GPIOs (none needed — spare inventory)

On headers, unused by the board: **1, 3, 12, 13** (+ **0** shared with BOOT, **43/44**
if UART0 is given up, **19/20** only if USB is given up). Wired-but-reclaimable inputs:
4 (TP_INT), 9 (RTC_INT), 18 (LCD_TE). Never usable: 26–32 (flash), 33–37 (octal PSRAM).

## 9. Open bench items `HW-GATED`

1. Boot a unit on USB-only power (no cell, no PWR-key press); confirm GPIO6/7 can be
   ignored by firmware (§6).
2. Confirm download-mode entry is clean from a power-cycle with the display initialized
   by prior firmware (§3 GPIO46 caution).
3. Bench-verify the 32-bit/RIGHT-slot mic capture against our own I2S init (not the
   demo's), on IDF at DES-3's chosen version.
4. Speaker acoustics in the printed case: grille + back-volume tuning; set the R57
   trimmer once and mark it (findings §2.4).
5. Factory image `Firmware/ESP32-S3-Touch-LCD-1.46.bin` kept as bench sanity-restore
   (findings §3.1).

## 10. Sources

- Official schematic PDF (p.1 GPIO matrix + per-circuit sheets): URL in the header.
- Vendor demo `waveshareteam/ESP32-S3-Touch-LCD-1.46` @ `fda89ff` — per-file/line cites
  inline; ESP-IDF 5.3.2 project (reading reference only, unlicensed).
- Waveshare wiki page `ESP32-S3-Touch-LCD-1.46B` (internal-connection tables; its mic
  table's "Buzzer" column header is a known cosmetic mislabel).
- ESP32-S3 Series Datasheet (§Boot Configurations, §2.3.4 GPIO restrictions,
  Table 2-14 flash/PSRAM pin mapping) + TRM ch.8 Chip Boot Control — via the
  espressif-docs MCP, 2026-07-17.
- `../design/assets/des7-hardware-findings.md` — enclosure data (2D print + STEP,
  hashes), mic porting evidence, vendor-software survey.

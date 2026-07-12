# Revox B215 — device dossier `[dev:revox-b215]`

Cassette deck (1985–~1990), automation by three Philips microcontrollers,
auto-calibration, NVM; serial link + IR receiver fitted as standard `[CONFIRMED]`.
Control path: **rear SERIAL LINK DIN, driven directly** (IR bypassed — serial reaches
"hidden" functions the handset lacks and gives status read-back). Shared family rules:
[`deck-common.md`](./deck-common.md); merge record: `docs/review/des1-truth-pass.md`.

**Status.** Pinout `[CONFIRMED]` from the B215 service manual §1.4; electrical nature
(bidirectional, opto-isolated, +5 V/150 mA) `[CONFIRMED]`. The research-era "RS-232 vs
TTL — CRITICAL VERIFY" question is **resolved: neither** (see §2). Outstanding: B205
frame captures + polarity (§7).

**Unit.** Genuine B215, serial 013773, Made in West Germany (Willi Studer GmbH,
D-7827 Löffingen), 45 W. Confirm B215 vs **B215S** behaviours where functions differ.
Two manuals apply: the **deck service manual** (pinout, transport, schematics) and the
separate **"IR Remote Control Systems"** manual, order no. **10.30.0430** (the
serial-link *protocol*: device identifier table, drive/aux function enumeration, status
string format; archive.org `studer_Revox_IR_Remote_System_Serv`).

---

## 1. Pin map `[CONFIRMED]` (SM §1.4 "Occupation des pôles de la fiche Serial Link")

| Pin | Manual definition | Use |
|---|---|---|
| **1** | GND (earth/terre) | chassis earth — **never the signal reference** |
| **2** | GND (**floating**/flottante) | **signal + opto reference ground** |
| **3** | **Serie I/O** (bidirectional serial data) | **DATA** — drive and read |
| **4** | +5 V (floating) | spare floating rail — leave unused |
| **5** | +5 V (**max 150 mA**) | **powers the satellite** |
| **6** | n.c. | unused |

![B215 SERIAL LINK pin assignment, SM §1.4](./img/serial-link-pinout.png)
![B215 rear panel](./img/rear-panel.png)

Two grounds and two +5 V pins are deliberate: reference everything to **pin 2**
(floating GND), power from **pin 5** — preserves the deck's internal optocoupler
isolation. The DIN body is standard; the manual lists a 6-pin assignment but most
builds mate a 5-pin 180° plug — **verify the socket variant before ordering**.

**IR-disable strap (short 1+2 and 4+5): hobbyist-sourced, NOT in the deck manual**
`[VERIFY]` — per the official pinout it bonds floating-GND to earth and ties the two
5 V rails; possibly how the deck senses "external controller present". Optional anyway
(only suppresses stray IR); scope/meter before applying.

## 2. Electrical layer `[CONFIRMED]` — the resolved research question

**NOT RS-232, NOT RS-485, not plain TTL UART.** A single **bidirectional open-collector
data line** (pin 3), idled high by the deck's internal pull-up, behind optocoupler
isolation inside the deck. ITT/Nokia pulse-coded framing with ~15 µs-scale features
(corroboration: IRMP #80 — ~15 µs bursts, 150/300 µs bit periods). The deck addresses
itself on this B200-series bus as **device identifier 04**.

> **CRITICAL SAFETY RULE `[CONFIRMED]`:** never drive pin 3 hard high. Assert = pull to
> pin 2; release = deck's pull-up restores high. Open-collector/open-drain stage only
> (ideally opto). Driving +5 V onto the line can damage the deck's output while it
> pulls low. (This is the retired REQUIREMENTS FR-14, kept as device truth.)

## 3. Wiring (bench-proven topology)

```
DIN pin 5 (+5 V) ─┬─[2.2–10 Ω]──┬── ESP32 5 V rail (100 µF + 0.1 µF at board)
                  │            1000 µF low-ESR (reservoir, deck-common §2)
DIN pin 2 (GND fl.) ────────────┴── ESP32 GND

control:  GPIO ──[1 kΩ]── PC817 LED → GND;  transistor C → pin 3, E → pin 2
status:   pin 3 ──[4.7 kΩ]── PC817 #2 LED (ref pin 2);  transistor → input-only GPIO
```

- GPIO high → opto conducts → pin 3 pulled low; GPIO low → line idles high. The opto
  inverts sense — final polarity is a firmware flag set after scoping (§7).
- Optional 4.7 kΩ pull-up on pin 3 ONLY if the scope shows weak idle-high.
- 6N137 instead of PC817 if edges look too soft.
- Status read-back parses the deck's return frames (play state, real-time mm:ss tape
  counter) — a genuine bonus of the serial path over IR.

## 4. Power behaviour `[CONFIRMED]` + wake mapping `[VERIFY]`

"Off" = **standby** (deck logic stays powered; the rear hard mains switch stays ON
permanently). "On" is modelled as **wake-on-transport**: sending Play wakes the deck and
acts (NEEO forum evidence). Whether Stop/Pause alone wake it is unconfirmed — bench
test decides the `standby` mapping (§7). **Auto-reverse is internal — no direction
command. Do not assume a serial eject exists** `[VERIFY]`.

## 5. Command surface (→ DES-4 descriptor)

`standby` (stateful switch), `stop`, `play`, `ff`, `rewind`, `pause`, `arm_record`,
`record` (momentary). Record behind the arm gate (deck-common §6). Optional extras if
the captures make them cheap: loop/positioning, cue, and the status read-back value
topics (play state, tape counter).

## 6. Firmware reference (for the future `boards/revox-b215` app)

The serial-link TX bit-bang has a working community reference:
`github.com/0815simon/revox-rc5-remote` (`revox_web_remote.ino`, ESP8266) — lift the
frame→GPIO-toggle core only (the repo is self-described trial-and-error; discard its
RC5/IR receive + webserver). Timing via µs busy-wait inside a brief critical section;
frame shape (start/0/1/repeat-gap) comes from the §7 captures against the 10.30.0430
enumeration.

## 7. Open bench items `HW-GATED`

1. Meter pin 5 → pin 2 ≈ +5 V with the deck powered (30-second sanity check).
2. **Scope-capture B205 frames on pin 3** (referenced to pin 2) for all §5 functions:
   idle level, swing, start-bit timing, 0/1 periods, frame length, repeat gap, bit
   order → command table + polarity flag. **Capture from a B205, not a B201** (the
   B201 doesn't drive Play on tape decks).
3. Wake test: from standby send Stop, then Pause, then Play — note which wake the deck
   (settles the `standby`/power-on mapping).
4. Verify B215 vs B215S; verify the socket's DIN variant.
5. Field note: a B215 transport auto-stopping ~4 s after engage was traced to a swapped
   microprocessor, not normal behaviour — if first Play "bounces", suspect
   framing/timing, not wiring.

## 8. Sources

- **B215 deck service manual** (Studer Revox, trilingual DE/EN/FR) — §1.4 rear panel +
  SERIAL LINK pin assignment.
- **Revox "IR Remote Control Systems" service manual 10.30.0430** — device id table
  (04 = B215), serial-link protocol, drive/aux function enumeration, status string
  format (archive.org `studer_Revox_IR_Remote_System_Serv`).
- `0815simon/revox-rc5-remote` (working TX reference; also the source of the
  unverified IR-disable strap idea); Tapeheads "Info on Revox Serial Link protocol
  wanted" (bidirectional single-wire warning, opto recommendation, Nokia/ITT family);
  IRMP discussion #80 (native waveform timing, TBA2800 preamp note); AudioKarma B215
  vs H1 thread (serial-only hidden functions); revoxremotes.com (commercial B215
  control — evidence the interface is fully characterizable); NEEO forum (PLAY
  triggers power-on).

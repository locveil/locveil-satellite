# Revox A77 Mk4 — device dossier `[dev:revox-a77]`

Reel-to-reel tape recorder (~1967–1977). Control path: **rear REMOTE CONTROL DIN,
momentary contact closure**. Shared family rules: [`deck-common.md`](./deck-common.md);
merge record: `docs/review/des1-truth-pass.md`.

**Status.** Pinout, contact logic, dummy-plug bridge and power pin `[CONFIRMED]` from the
A77 service manual (10.18.1611, §7.1 Fig. 7.1-86 and §5.9 Table 5.9-44). Open bench items
in §8. Do a 30-second continuity check of the socket before connecting — the schematic is
authoritative, the check is cheap insurance.

---

## 1. Architecture

Solid-state, **electromechanical relay logic** — no microcontroller, no IR receiver, no
command bus. `[CONFIRMED]` Transport = 3 relays (A, B, C) + a Record Relay +
roller/brake solenoids (§5.9). The deck was designed for momentary-contact wired remote
of all functions: remote contacts F3…F10 simply **parallel the front-panel button
contacts**, steered by diodes. Switches are momentary/non-latching. No auto-reverse (no
direction command). **No soft power** — hard mechanical mains switch, not automated.

## 2. Connector & pin map `[CONFIRMED]` (SM Fig. 7.1-86)

Rear socket #25: **Hirschmann WIST 10** (10-pin DIN). Each button closes a **pin PAIR**
(a floating SPST closure between two pins — NOT a switch to a single common rail; the
research-era "switch common" wording was wrong, see the truth pass).

| Function | Closes pins | Wire colours | Notes |
|---|---|---|---|
| `<<` REWIND | **8 – 9** | gry – wht | plain closure |
| `>>` FAST-FWD | **10 – 3** | blk – org | RC net (22 Ω + 10 k + 500 µF) + steering diode in the remote |
| PLAY | **4 – 5** | yel – grn | plain closure (+ steering diode) |
| STOP | **1 – 2** | brn – red | RC net; **the dummy-plug pair** |
| REC | **6 – (PLAY)** | blu | fed via PLAY; assert together with PLAY |
| **+27 V out** | **7** | vio | **150 mA max** — feeds the buck, never the ESP32 directly |

Pin colours 1–10: brn, red, org, yel, grn, blu, vio, gry, wht, blk; centre pin "sw" =
chassis/screen. **Dummy plug shorts 1–2** — the manual says verbatim it "must be inserted
for operation without the REMOTE CONTROL unit"; keep that bridge in the adapter (the
STOP opto simply parallels the same pair).

![A77 REMOTE CONTROL schematic, Fig. 7.1-86](./img/remote-schematic.png)

## 3. Relay truth table `[CONFIRMED]` (SM Table 5.9-44)

| Mode | Relay A | Relay B | Relay C | Record Relay | Roller Sol. | Brake Sol. |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| STOP | – | – | – | – | – | – |
| PLAY | yes | – | – | – | yes | yes |
| `>>` FF | – | – | yes | – | – | yes |
| `<<` REW | – | yes | – | – | – | yes |
| REC | yes | yes | – | yes | yes | yes |

**REC = A + B + Record Relay → Record depends on the PLAY path**; in the remote wiring
REC is diode-steered so pressing REC alone does nothing. **Record requires PLAY + REC
asserted together — preserve this, never defeat it.**

![A77 Table 5.9-44 relay/solenoid truth table](./img/function-table.png)

## 4. Power tap

- **Pin 7 = +27 Vdc, 150 mA max** `[CONFIRMED]` (documented as a slide-projector
  supply; fed by the 27 V rail, violet DF1, that also drives the transport board).
- **27 V → 5 V switching buck** (≥30 V input; MP1584/LM2596 class) — a linear drop
  would burn ~2 W. Budget: ESP32 Wi-Fi peak ≈ 1.7 W ≈ ~65 mA at 27 V through the buck —
  comfortable inside 150 mA. Reservoir network per deck-common §2 at the buck output;
  **fuse the pin-7 tap 100–200 mA**.
- The only deck of the four workable **entirely from the back panel** — no internal
  soldering.

## 5. Isolation

Linear mains-transformer supply, rails ~21 V and 27 V `[CONFIRMED]`. DC ground is
**not** chassis (service community explicitly warns against chassis as measurement
reference) → isolated secondary `[CONFIRMED-ish]` — still `[VERIFY]` secondary-gnd vs
earth on the actual unit (deck-common §3). Contact pins stay isolated from the board by
the opto-MOSFETs regardless of powering.

## 6. Command surface (→ DES-4 descriptor)

`stop`, `play`, `ff`, `rewind`, `arm_record`, `record` — all momentary (pushbutton).
No power/standby control. Optional read-only values once the §7 sensor exists:
`reels_moving`, `tape_counter`, `end_of_tape`.

Emulation: pulse the pair's opto-MOSFET ~150–250 ms (bench-tune). Record = PLAY + REC
optos together for the press window, behind the arm gate (deck-common §6).

## 7. Reel-motion interlock (the A77-specific hazard)

**Problem:** PLAY while reels still coast from a fast wind → pinch roller grabs fast
tape → spill/stretch. The A77 has **no motion sensor** — §5.9 shows only the
photoelectric end-of-tape switch (LDR + lamp) `[CONFIRMED]` — the B77 added one to
solve exactly this (its motion-sense line reads "stopped" ~0.5 s after actual halt).

**Fix (firmware interlock, reversible, no deck surgery):** add a sensor the board
reads — IR-reflective (TCRT5000 + contrast mark on a reel hub) or Hall + magnet on the
brake-drum (more robust to light/dust); precedents: B77, factory ITAM 3.77. Input-only
GPIO is fine for it. Logic: on `play`/`record`, if moving → assert STOP, wait for
motion to cease (timeout ~8 s), wait `POST_STOP_DELAY` ~500 ms (B77-style settle),
then engage. Refusal = command fails.

**Known limitation (by design):** only the board's own commands are gated; front-panel
presses bypass it (that path never touches the board). In-deck protection would be a
B77/ITAM-style hardware mod — out of scope.

> Unrelated repairs, don't conflate: sluggish end-of-tape auto-stop = aged LDR R155 /
> relay-board R118; weak rewind torque with 18 cm reels = §8.1 mod (R125 820 Ω → 1.2 kΩ
> 9 W on drive control 1.077.370).

## 8. Open bench items `HW-GATED`

1. Continuity-check every §2 pin-pair against the actual socket (deck unpowered).
2. Measure pin 7 ≈ 27 V and that it holds under the buck's load; verify
   secondary-gnd ≠ chassis/earth on this unit.
3. Pick the reel-motion sensor + mounting point; tune motion debounce (~400 ms
   starting point), `POST_STOP_DELAY` (~500 ms), press pulse width (~150–250 ms).
4. Bench-confirm REC = PLAY+REC behaviour on the actual Mk4.

## 9. Sourcing note — the WIST 10 connector

The scarce, expensive part of the whole build. Routes: (1) genuine plug from Revox
Service Villingen / Klassik Audio CH (~EUR 25 min-order, ask for a blank/unwired one);
(2) **PCB-in-WIST10-footprint** — small PCB cut to the plug outline with **1.4–1.5 mm
pins** in the contact pattern (revoxforum.ch "WIST10 Stecker Ersatz", builder "hbose",
~EUR 4; pin diameter is the hard constraint, measure the socket); (3) one integrated
PCB carrying pins + optos + module — the end state, design only after validating
contact geometry via route 2. Route 2/3 is the natural shape for this repo's
`boards/revox-a77/` project.

## 10. Sources

- **A77 service manual 10.18.1611** — §7.1 Remote Control Fig. 7.1-86 (connector, pin
  map, +27 V pin 7, dummy plug); §5.9 Drive Control + Table 5.9-44 (relay truth table);
  archive.org `studer_Revox_A77_Serv`; ManualsLib/Manualzz mirrors.
- siber-sonic A77 repair tips (dummy plug, rails; links to the Obsolete-Media "A77
  Remote Control Plug" pinout page); Tapeheads PSU threads (21/27 V rails, DF1 violet,
  "don't use chassis as reference").
- revoxforum.ch "WIST10 Stecker Ersatz" (hbose PCB adapter); revoxremotes.com commercial
  adapter (confirms contact emulation is sufficient); Tapeheads B77 threads (motion-
  sense timing model, REC-via-PLAY diode steering corroboration).

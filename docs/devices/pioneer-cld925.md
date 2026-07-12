# Pioneer CLD-D925 — device dossier `[dev:pioneer-cld925]`

CD/CDV/LaserDisc player (1996). Control path: **rear CONTROL IN 3.5 mm minijack
(Pioneer SR / System Remote), baseband IR** — the easiest of the four decks: no opening
the unit for signal, no protocol reverse-engineering. Shared family rules:
[`deck-common.md`](./deck-common.md); merge record: `docs/review/des1-truth-pass.md`.

**Status.** SR electrical interface and protocol `[CONFIRMED]` from the definitive
reverse-engineering analysis (see §6 sources) — the research-era "`[VERIFY]` the
waveform" is resolved. Outstanding: per-unit scope confirmation + rail metering (§5).

---

## 1. How Pioneer SR CONTROL IN works `[CONFIRMED]`

SR is **a wired IR repeater built into the gear**: CONTROL OUT carries the
**demodulated (carrier-stripped) copy of whatever IR the receiver saw**; CONTROL IN
accepts that same baseband signal *instead of* the built-in IR sensor.

- **Connector:** 3.5 mm **mono** jack (JA3/JA4, part RKN1004) — tip = signal, sleeve =
  "ground" *but see the ground quirk below*.
- **Idle:** tip ~+5 V. **Open-collector with internal pull-up** — CONTROL IN measured
  ~**100 kΩ** (OUT ~10 kΩ). Pull the tip low to signal; release to restore high.
- **Protocol-agnostic at the waveform level:** the tip carries the identical signal a
  demodulating IR receiver outputs; it repeats any remote's codes.
- **Plugging in disables the internal IR sensor** (RC-IX behaviour) — no
  double-triggering.
- **The sleeve is NOT grounded** — Pioneer deliberately floats it (avoids ground loops
  between chained units). **A ground reference must be supplied separately** — the #1
  reason an SR attempt "does nothing".

Internal fallback (never needed if the jack works, `[CONFIRMED]` from the service
manual): IR module **GP1U28X** on the PWSB assy via **CN301** (9-pin 1.25 mm FJ), output
idle-high/active-low, 5 V domain; remote stream lands at mode-control IC
**PD3337A = IC101** pin 28 ("SEL IR"), 5 V CMOS. Same open-drain wired-AND injection
pattern would apply at that node.

## 2. Wiring

```
GPIO ──[1 kΩ]── PC817 LED → GND        (bare NPN BC547/2N3904 also fine)
PC817 transistor C → 3.5 mm TIP  (CONTROL IN tip)
PC817 transistor E → ground reference (see quirk)
```

**Ground quirk:** tie board ground to player ground by another path — easiest is an
existing **RCA A/V cable's shield** between player and system; otherwise a dedicated
wire to a chassis screw / RCA shell.

**Polarity `[CONFIRMED]`:** carrier-stripped IR is **active-low** (like a demodulating
receiver's output: idle high, pulse low during bursts). Firmware emits the *inverted*
raw-IR logic: 38 kHz burst → pull LOW; gap → release HIGH.

## 3. Power tap

The jack carries **no usable supply** (the ~5 V idle is the weak 100 kΩ pull-up —
microamps). Tap an **internal +5 V logic secondary rail** (near IC101 / a logic
connector), isolated SMPS secondary `[CONFIRMED]` — the PCB explicitly marks
PRIMARY/SECONDARY; **never probe the primary**. Two install styles:

- **Option B — power pigtail through the case grommet (recommended, least invasive):**
  two wires (5 V + GND) from the rail straight to the box; factory mono jack untouched.
- **Option A — upgrade CONTROL IN to a TRS jack:** tip = signal, ring = +5 V (new
  wire), sleeve = GND (new wire — also fixes the ground quirk); one stereo cable to the
  box, but three internal solder joints.

Either way: reservoir network per deck-common §2 at the box end; **meter the rail under
the satellite's load — specifically the sustained OTA draw, not just a command burst**
`[VERIFY]`; don't hang the module raw on the rail that feeds the mode controller.

## 4. Command surface (→ DES-4 descriptor)

`power` (switch — confirm discrete on/off vs toggle on the remote), `play`, `pause`,
`stop`, `scan_fwd`, `scan_rev`, `chapter_next`, `chapter_prev` (momentary). Optional:
display/OSD, open/close, side-change (LD-specific — confirm the remote exposes it).
**No status read-back** — SR CONTROL IN is one-way; status would be a separate tap,
out of scope.

**IR codes: reuse the proven Wirenboard IR-blaster captures** (deck-common §4) — same
data, carrier off; replicate the remote's repeat frame / double-send where a single
shot is flaky. Original handset family for fresh captures if ever needed: CU-CLD.

## 5. Open bench items `HW-GATED`

1. Scope CONTROL IN on the unit: tip idles ~5 V; capture the baseband reference from
   CONTROL OUT (or the internal receiver output) on a real remote press; meter sleeve →
   chassis to confirm it is NOT 0 Ω.
2. Meter the +5 V rail under bridge load (light-sleep + reservoir in place) — no sag.
3. Verify secondary-gnd vs earth on this unit (deck-common §3).
4. Decide power Option A vs B before opening the deck.

## 6. Sources

- **"Hacking Wired Remote Control Jacks Into A/V Equipment"**
  (wiredremotecontrol.blogspot.com, John Sevinsky) — the definitive SR analysis: idle
  ~5 V, open-collector, IN ~100 kΩ / OUT ~10 kΩ, baseband IR copy, repeats any remote,
  sleeve not grounded, RC-IX disables internal sensor.
- **CLD-D925 service manual** (order RRV1546; ManualsLib mirror p.52 = mechanism-
  control IC pin table; manuals.lddb.com / elektrotanya scans) — CONTROL jack part ids,
  GP1U28X/CN301, PD3337A pin table, PRIMARY/SECONDARY markings.
- AudioKarma / Steve Hoffman threads (SR jack corroboration on LD/CD gear).

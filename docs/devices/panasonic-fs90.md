# Panasonic NV-FS90 — device dossier `[dev:panasonic-fs90]`

S-VHS Hi-Fi VCR (~1990). Control path: **an ADDED rear CONTROL IN jack** — the FS90 has
**no factory wired-control port** `[CONFIRMED]` (AV1/AV2 SCART + IR only; the research-era
"does an edit terminal exist?" is resolved: it doesn't — those were pro AG-series
features). The build recreates the Pioneer SR interface by a **parallel no-cut tap on
the internal IR-receiver output**; once the jack exists, output stage, firmware and
codes are **identical to the Pioneer build** ([`pioneer-cld925.md`](./pioneer-cld925.md)).
Shared family rules: [`deck-common.md`](./deck-common.md); merge record:
`docs/review/des1-truth-pass.md`.

**Status.** Architecture `[CONFIRMED]` (IR receiver module → baseband output → syscon
input; scanned-matrix front panel — which is exactly why the IR node is the tap, not the
matrix). The IR receiver's OUT pin is **deliberately not quoted from the manual** — it
is identified on the actual board before soldering (§4.1). Power-isolation verification
remains the **gating** bench item for this deck (§5).

---

## 1. Internal control architecture `[CONFIRMED]`

- Remote path: **IR receiver module → baseband logic-level output (idle-high,
  active-low) → input port on syscon IC6001**, a Panasonic MN153xx-family micro on
  5 V logic (the related NV-VP60 service manual flags IC6001 pin 37 as the 5 V rail —
  establishes the generation's logic level).
- **Front panel is a scanned key matrix** (syscon/counter micros) — injecting into a
  scanned matrix means hitting the right row/column at the right scan instant; the
  IR-OUT node feeds the syscon the baseband bytes it already decodes. The IR node is
  the easy, correct tap.
- That node behaves like Pioneer CONTROL IN: idle ~5 V, open-collector-ish, baseband,
  active-low — two open-collector drivers **wire-OR** safely, so a parallel tap needs
  no cut.

## 2. The added jack (parallel tap, no cut — chosen approach)

```
IR receiver module (3-pin, behind the front window)
  Vcc (~5 V) ── the +5 V tap for box power (ring)
  GND        ── new jack SLEEVE (and deck ground)
  OUT        ─┬─ existing trace to IC6001 input   (LEAVE CONNECTED)
              └─ new jack TIP (injected signal, parallel)
```

- **Switched (closed-circuit) panel-mount 3.5 mm TRS jack** on the rear panel (drill a
  clear spot; wire only tip+sleeve[+ring] now). The switch contact stays unused — it
  keeps the free upgrade path to a cut/auto-mute install if stray IR ever becomes a
  nuisance.
- **TRS carries everything on one cable:** tip = signal, ring = internal +5 V, sleeve =
  GND. Unlike the Pioneer, **this jack is ours — DO ground the sleeve** to the deck for
  a proper return.
- **Reversible:** remove the tap wire and jack → deck is exactly stock.
- **Accepted trade-off:** the internal IR sensor stays live — a stray remote / strong
  ambient IR can still reach the deck.

## 3. Command surface (→ DES-4 descriptor)

`power` (switch — confirm discrete vs toggle), `play`, `stop`, `pause`, `ff`, `rewind`,
`arm_record`, `record` (momentary; record behind the arm gate, deck-common §6).
Optional: eject (confirm the remote exposes it), channel ±, OSD. **No status
read-back** (IR path is one-way; transport status would be a separate FIP/syscon tap —
out of scope).

**IR codes: reuse the Wirenboard IR-blaster captures** (deck-common §4) — Panasonic
protocol family (Kaseikyo/"Panasonic" 48-bit typical), no decoding needed, replay raw
timings carrier-off; Panasonic frames often expect the standard repeat/spacing — mimic
the blaster's held-button behaviour if a single shot is flaky. This deck is *why* the
wired path exists: the awkwardly-placed FS90 is where the air-gap blaster was least
reliable.

## 4. Bring-up specifics

### 4.1 Identify the IR-receiver OUT pin (FIRST, meter/scope, before soldering)

Power the deck; find the 3-pin module behind the front IR window (SM helps locate it).
One pin = GND (0 V), one = Vcc (~5 V steady) — note it, it's the power tap. The third
is OUT: idles near 5 V; on a remote press a meter on AC volts twitches and a scope
shows clean **active-low baseband pulses, no 38 kHz carrier**. That confirms both the
tap pin and the polarity. **Never trust a quoted pin number for a solder point.**

### 4.2 Order of operations

Deck unplugged → solder tap wires (OUT + Vcc + GND), fit the jack → power up →
**confirm the deck still answers its own remote** (proves the parallel tap didn't
disturb the node) → meter the 5 V rail under the box's load → first live test Play,
then Stop/Pause/FF/Rewind, **record last** (gated).

## 5. Open bench items `HW-GATED` — including the gating isolation check

1. **Rail isolation — non-negotiable, gates the whole power approach** (carried from
   the research pass; the build docs under-weighted it): before tapping anything,
   meter the candidate 5 V rail's ground against mains earth AND chassis, power-off
   then power-on. Panasonic supplies of this era are transformer-based with multiple
   `UNREG_*V` secondaries `[INFERRED]`, but a VCR is exactly the class where a
   non-isolated or hot section is plausible. **Assume mains hazard until proven
   otherwise; never probe the primary.** If the syscon rail is NOT cleanly isolated:
   fall back to an isolated DC-DC from whatever rail exists, or (violating
   power-from-device for this one deck) a small external supply + fully optoisolated
   injector. Do not force the requirement onto a non-isolated rail.
2. Identify the IR-receiver OUT pin on the actual board (§4.1).
3. Meter the +5 V tap under the satellite's load (reservoir network in place).
4. Confirm which functions the remote exposes discretely (power, eject).

## 6. Sources

- **NV-FS90 service manual** (HiFi Engine / elektrotanya / eserviceinfo / archive.org
  `manual_NVFS90BEB_SM_PANASONIC_GB`) — IR module + syscon location; connection docs
  confirm AV1/AV2 SCART + IR only, no wired port.
- **Panasonic NV-VP60 service manual** — IC6001 (MN153xx family), 5 V rail pin 37:
  the generation's logic-level anchor.
- **Panasonic AG-500 service manual** — the standard Panasonic VCR scanned-key-matrix
  architecture (why the matrix is the hard path).
- **"Hacking Wired Remote Control Jacks Into A/V Equipment"**
  (wiredremotecontrol.blogspot.com) — the canonical add-a-CONTROL-IN recipe; the
  parallel no-cut variant here follows its JVC example (Mitsubishi = series/switched
  variant).
- digitalFAQ VCR-repair + Tapeheads Panasonic PSU threads (`UNREG_*V` secondary
  topology of late-80s Panasonic supplies).

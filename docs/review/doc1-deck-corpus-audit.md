# DOC-1 — deck-corpus audit: is `deck-common.md` truly the common truth?

**Task.** Owner-filed 2026-07-17: the four deck dossiers are "not that 100 %" verified
(unlike the waveshare dossier); audit `docs/devices/deck-common.md` against
`revox-a77.md` / `revox-b215.md` / `pioneer-cld925.md` / `panasonic-fs90.md` —
specifically whether the common doc truly contains the common pieces. **Ground rule
(owner): on contradiction, the dossiers win.** The waveshare dossier is out of scope
(untouched; it is not part of the deck family — deck-common's scope line enumerates
exactly the four decks, so its presence in `docs/devices/` creates no conflict).

**Method.** Claim-by-claim pass over deck-common §1–§7, each claim tested three ways:
(a) does it actually hold for all devices it claims to cover, (b) does any dossier
contradict it, (c) is it chip-truth that can be re-verified against official Espressif
docs (re-verified 2026-07-17 via the espressif-docs MCP — sources cited inline). Plus
the reverse pass: content duplicated across dossiers that belongs in common, and
device-specific truth leaked into common.

**Verdict up front.** The common doc is structurally sound — its device-name mentions
are pointers, not leaked truth, and its §4/§6/§7 conventions genuinely hold family-wide.
But it carries **two real contradictions with dossiers (F-1, F-2 — dossiers win), one
wrong chip figure (F-5), one stale referent (F-6)**, and the B215 dossier has **two
gaps against common rules (F-3, F-4)**. Remediation is filed as **DOC-2**; nothing found
is bench-blocking (all fixes are documentation).

---

## Findings — contradictions (dossier wins)

### F-1 `[CONTRADICTION]` common §1 "deck-derived only" vs FS90 §5.1 sanctioned fallback

Common §1 is absolute: *"Power: deck-derived only — no wall plugs, no USB, no PoE."*
The FS90 dossier's **gating** bench item §5.1 explicitly sanctions the exception: if the
syscon rail is not cleanly isolated, *"(violating power-from-device for this one deck) a
small external supply + fully optoisolated injector"* — and forbids forcing the
requirement onto a non-isolated rail. The dossier is right: the power rule must never
outrank the isolation safety gate. **Fix (DOC-2):** common §1 gets the exception
pointer — "deck-derived by default; a dossier's isolation gate may force the external-
supply fallback (FS90 §5.1)".

### F-2 `[CONTRADICTION]` common §2 reservoir topology vs B215 §3 bench-proven wiring

Common §2 places the **2.2–10 Ω inrush resistor "in series with the big cap"** (i.e. an
R+C branch hanging off the rail, board fed directly). The B215 dossier's §3 diagram —
headed *"bench-proven topology"* — wires it the other way: **resistor in the feed, the
1000 µF low-ESR reservoir downstream of it, directly across the board rail**:

```
DIN pin 5 ──[2.2–10 Ω]──┬── ESP32 5 V rail
                      1000 µF
```

The bench topology is also the electrically coherent one: a low-ESR cap can only soak
the 300–500 mA TX spikes if it sits directly across the board's rail; putting 2.2–10 Ω
in series with the cap defeats exactly the low-ESR property §2 calls load-bearing, and
leaves the deck rail exposed to the spikes the network exists to hide. R-in-feed gives
both inrush limiting at power-up and spike decoupling in operation; the voltage drop
across the feed resistor is small at the true average draw (see F-5). The A77 dossier
defers to "deck-common §2" wording, so the wrong factoring propagates silently.
**Fix (DOC-2):** reword common §2 to the B215 (feed-series) topology; A77's reference
then heals itself.

## Findings — gaps (common rule not reflected in a dossier)

### F-3 `[GAP]` B215: the 150 mA rail has no fuse anywhere in its dossier

Common §2: rails rated ~150 mA get a **100–200 mA fuse on the tap**, *"apply the same
thinking to every tap"*. The B215's pin 5 is **"+5 V (max 150 mA)"** `[CONFIRMED]` — the
exact case the rule names — yet the §3 wiring diagram and §7 bench list carry no fuse.
**Fix (DOC-2):** add the fuse to B215 §3 (additive — no dossier truth contradicted).

### F-4 `[GAP]` B215: no ground-vs-earth/chassis meter check in its bench items

Common §3 mandates the power-off/power-on meter check of the candidate rail's ground
against mains earth AND chassis **"`[VERIFY]` on every unit"**. A77 §5/§8, CLD925 §5.3,
FS90 §5.1 all carry it; **B215 §7 does not**. The B215's floating ground is
`[CONFIRMED]` from the service manual (pins 1 vs 2), which explains but does not
discharge the per-unit rule — manuals describe design intent, the meter check catches
this unit's reality (previous-owner mods, leakage, a bonded strap — note the dossier's
own unverified IR-disable strap bonds pin 1 to pin 2, exactly the kind of thing the
check would surface). **Fix (DOC-2):** add the §3 meter check to B215's bench list.

## Findings — wrong or stale content in common

### F-5 `[INACCURACY]` common §2: "average draw ≈ 15 mA" is not an ESP32 number

Official ESP-IDF low-power guide for the classic ESP32 (verified 2026-07-17,
`docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/low-power-mode/low-power-mode-wifi.html`):
Wi-Fi **auto light-sleep average = 3.34 / 2.33 / 2.19 mA** (DTIM1/3/10); modem-sleep is
29–31 mA. 15 mA matches neither — it is verbatim the **ESP8266** datasheet's
modem-sleep DTIM3 figure ("requires about 15 mA", ESP8285/8266 datasheet §Power
Management), which is almost certainly the research-era source. The error is
*conservative* (rails sized to 15 mA idle are oversized, not undersized), so nothing
built against it is unsafe. **Fix (DOC-2):** correct to the official ~2–4 mA
light-sleep average, keep 15 mA explicitly as a deliberate sizing margin if wanted, and
keep the real sizing drivers (TX spikes, sustained OTA draw) as stated.

### F-6 `[STALE REFERENT]` common §5: "Legacy pin choices in the dossiers"

*"Legacy pin choices in the dossiers are `[INFERRED]` starting points, not
commitments"* — but **no deck dossier contains a single GPIO assignment** (DES-1
deliberately stripped them; the only pin numbers anywhere are the GPIO14 anecdote's, in
common itself). The caution is right, its referent is empty. **Fix (DOC-2):** reword to
point at where legacy pins actually live (the retired single-image sources under the
deleted `imports/` tree, resolvable at `0d950a9`) — or simply state "pin maps do not
exist yet; they are authored per-app at FW time and audited per DES-3".

## Findings — verified clean (no action)

- **F-7 common §5 chip truths re-verified** against the ESP32 datasheet/TRM/IDF docs:
  straps are GPIO0 (WPU) / GPIO2 (WPD) / GPIO5 (WPU) / GPIO12=MTDI (WPD) / GPIO15=MTDO
  (WPU) — datasheet §Boot Configurations Table 3-1; GPIO34–39 input-only with **no
  output driver and no internal pulls** — datasheet Appendix A note 2, TRM IO_MUX table
  (reset code 0, note I); **GPIO14 = MTMS, weak pull-up at reset** — TRM IO_MUX table
  (reset code 3 = IE+WPU). Every §5 claim stands.
- **F-8 §4/§6/§7 conventions hold family-wide:** open-collector/never-drive-high fits
  B215/CLD925/FS90, with the A77 contact-closure case correctly carved out in §4
  bullet 2; record-arming is correctly conditional ("any device exposing `record`" —
  A77/B215/FS90 have it gated, CLD925 has no record); the §7 negatives contradict no
  dossier (three decks' `power`/`standby` verbs are soft/standby control, not the mains
  switching §7 excludes; the A77 correctly exposes no power verb at all).
- **F-9 no device truth leaked into common:** every device mention in common (§2 A77
  fuse example, §3 Panasonic gating, §4 subfamily scoping, §6 interlock names, §7 A77
  mains note) is a pointer to a dossier, not a duplicated fact. Correct placement.
- **F-10 cross-dossier reuse is acceptable as-is:** the Pioneer-SR interface truth
  (idle-high ~5 V, open-collector, carrier-stripped active-low) lives in
  `pioneer-cld925.md` with `panasonic-fs90.md` importing it by explicit link ("identical
  to the Pioneer build") — an explicit 2-of-4 link beats promoting a non-family-wide
  claim into common. Leave.

## Minor (fold into DOC-2 opportunistically)

- **F-11 `[DUPLICATION]`** B215 §3 inlines the reservoir component values that common
  §2 owns (it cites §2 but repeats the numbers — a staleness risk exactly like the F-2
  divergence that already happened). After the F-2 reword, trim B215's inline values to
  the diagram + "values per deck-common §2". The PC817+1 kΩ opto stage appears in
  B215 §3 and CLD925 §2 (FS90 inherits via Pioneer) — optionally hoist "default opto
  stage: PC817 behind 1 kΩ; 6N137 if edges are soft" into common §4 and keep only
  deviations in dossiers. Low priority; both are hygiene, not correctness.

## Sources

- The five corpus docs at HEAD (`docs/devices/deck-common.md` + four dossiers).
- ESP32 Series Datasheet §Boot Configurations + Appendix A; ESP32 TRM ch.6 IO_MUX pin
  list (reset configurations); ESP-IDF esp32 low-power-mode Wi-Fi guide (DTIM current
  table); ESP8285 datasheet §Power Management (provenance of the 15 mA figure) — all
  via the espressif-docs MCP, 2026-07-17.

# Voice-satellite enclosure — waveshare-lcd146 wall case (DES-8)

Status: **AGREED 2026-07-18** (interactive owner session). CAD source:
`enclosures/waveshare-lcd146/case.py` (build123d, INFRA-2 toolchain); print/fit/acoustic
iteration: **DES-9** (HW-GATED). Basis: vendor STEP + 2D print, re-downloaded and
hash-verified against `assets/des7-hardware-findings.md` §2.1; every position below is
MEASURED from the STEP (build123d survey), not transcribed.

## 1. Decisions (owner, 2026-07-18)

| # | Decision |
|---|---|
| C-1 | CAD toolchain = **build123d** (INFRA-2: `~/cad/build123d-env`, distro python; over CadQuery/OpenSCAD — native STEP import let the survey measure the real assembly) |
| C-2 | Mount = **keyhole slots** (2×, screw-head Ø7 entry), back flat on the wall; metal kept LOW — the antenna band is the board top |
| C-3 | Cable exit = **variant B: straight plug, open bottom** — any straight A-to-C cable works (the recorded cable purchase: straight, data-capable); ~19 mm plug visible below the case |
| C-4 | Body = **squircle** following the board outline: 45.1 × 48.5 mm face, **15.9 mm off the wall**, corner R≈20 |
| C-5 | Openings **bottom-only** (mic inlet Ø1.8 + 3 speaker slots + USB aperture) — face and silhouette clean |
| C-6 | Material = **matte white PETG**, all three units |
| C-7 | Bezel lip opening Ø38.2 — stays outside the Ø37.36 viewing circle, protects the glass-less panel edge |
| C-8 | Two parts: **front shell** (bezel + walls) + **back plate** (keyholes, M2 screws into the board's SMTSO standoffs, acoustic ribs); board screws to the plate, plate hangs on the wall |
| C-9 | Switch access = **service pinholes** (Ø1.6, right wall at the measured switch positions) — BOOT/PWR are bench acts, not user controls |

## 2. Measured inputs (STEP survey 2026-07-18; frame = board centre, X right, Y up, Z out of face)

| Item | Value |
|---|---|
| Board / stack | 39.36 × 41.53; face Z −1.89, PCB back −7.68, deepest metal (header pins) −12.95 |
| Mic (fixed) | MSM261S4030H0R **soldered on the back face** at (−14.20, −12.05), body 0.9 proud, top-ported → fires at the WALL |
| Speaker (fixed) | 12 × 10 × 2.8 **pad-soldered on the back face** at (+11.17, 0.00), rear-firing — *corrected in-session (owner catch): earlier "wired/relocatable" reading was wrong; the STEP places it as a PCBA child like the mic* |
| USB-C | bottom centre (0, −19.20), shell 8.94 × 7.60, Z −6.58…−10.64 |
| Switches | TS24CA ×2, actuators at the +X edge, y = +9.91 / −10.20, z −8.10 |
| M2 standoffs | SMTSO-M2-3.5 at **(12.00, −14.95), (−11.54, −15.45), (0.00, +17.75)**, outer ends Z −10.90 |
| Viewing circle | Ø37.36 (active Ø36.96) — nothing covers inside it |
| Antenna | top band (~y > +17) — plastic only near it; keyholes placed at y = −6 |

## 3. Acoustic architecture (the §2.4 "dominant quality lever", wall-posture resolved)

Both transducers are soldered to the back face and fire at the wall; the case relocates
nothing and instead forms two sealed paths that turn 90° to the bottom edge:

- **Mic**: a rib ring on the back plate (outer Ø4.4 — lands fully on the 4.7 × 5.0
  can) seals against the MIC CAN'S PORTED FACE (Z −8.60; the can sits 0.9 proud of
  the board — a board-plane ring would crash into it, the v0 bug caught 2026-07-19)
  via a compliant washer: adhesive closed-cell foam or punched silicone, ~Ø4.5 ×
  0.8 mm compressed to the 0.5 mm gap, bore ~Ø1.5 over the port. Inside the ring the
  path is an **acoustic L** (owner-caught 2026-07-19: a straight vertical bore
  dead-ends in the plate while the duct hits the ring's solid side): Ø1.8 bore from
  the gasket face down to channel height, a side passage through the ring wall, then
  the 2 mm rail channel to the bottom-edge inlet. Both paths are probe-walked
  end-to-end in verification (33 + 42 points, all open).
- **Speaker**: a rib box seals around the speaker in place (same gasket principle); a
  5 mm opening in its bottom rib — **offset left to x 7.5, because the lower-right
  SMTSO pillar (12.00, −14.95) sits dead on the centred line (probe-caught
  2026-07-19)** — feeds a duct to **three 1.6 mm bottom slots**. Small sealed back
  volume; the ~20 mm duct trades some treble — voice-prompt acceptable, bench-tuned
  in DES-9 (slot count/width are parameters; the sealed-duct design must skirt the
  pillar likewise).
- Radiating-face check (which speaker side is the diaphragm) is a DES-9 first-print
  item — read from the STEP part or the physical unit before sealing rib heights.
- Mic **port-offset check** (DES-9, with the datasheet/unit in hand): top-ported cans
  often place the sound hole OFF-CENTRE on the lid — v0 centres the ring bore on the
  can; align the bore (and the gasket washer's bore) to the real hole before print 2.
- The mic duct is a **closed tunnel** since 2026-07-19 (owner question — isolation:
  one defined path instead of coupling the mic to the case cavity; the 2 mm roof
  bridge is trivial FDM). Remaining DES-9 seam: the rim hand-off pocket where the
  tunnel meets the shell's inlet (plus the 0.15 rim clearance) — gasket detail.

## 4. Parts & assembly

1. Back plate screws to the board's three SMTSO-M2 standoffs (M2×6, countersunk from
   the wall side; screw budget respects the 3.5 mm max engagement).
2. Front shell caps over board + plate (side-wall capture; retention feature — snap
   lip vs 2 self-tappers from below — is a DES-9 print-fit decision, v0 is friction).
3. Plate hangs on two wall screws through the keyholes; USB cable exits the open
   bottom aperture (11 × 6 mm) with a straight plug.

## 5. Follow-ups

- **DES-9** (HW-GATED): print v0, fit-check on a unit, radiating-face check, gasket
  material pick, retention feature, acoustic bench (mic SNR through the duct vs open;
  speaker slot tuning), then CAD amendments here. Print orientation: face-down front
  shell, inner-face-up plate; no supports expected except the USB aperture bridge.
- Cable purchase (recorded): straight **USB-A → USB-C data-capable** cables + plain
  **5 V/2 A USB-A** wall adapters, three of each.

## 6. Session evidence

Concept sheet (non-normative visualization, incl. the two cable-exit variants the
owner decided between): claude.ai artifact `50bfdc56` (session 2026-07-18). The
normative record is this document + `case.py`.

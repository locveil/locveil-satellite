# Deck-device satellites — shared design rules (harmonized, DES-1)

**Scope.** The four vintage AV transports controlled by per-device ESP32 satellites:
[`revox-a77`](./revox-a77.md), [`revox-b215`](./revox-b215.md),
[`pioneer-cld925`](./pioneer-cld925.md), [`panasonic-fs90`](./panasonic-fs90.md).
This doc is the family-wide engineering truth; the dossiers hold per-device facts.

**Provenance.** Harmonized 2026-07-12 (DES-1) claim-by-claim from the bridge-era corpus
(four bench/manual-confirmed build docs + one general research doc; merge record:
`docs/review/des1-truth-pass.md`). The bench-confirmed build docs are **leaf truth** — a
newer, more general claim never downgrades them. Firmware architecture statements from
that era are superseded by HK-4: **per-device apps from shared `components/`**, never a
single multi-device image (`per-device-apps`; the GPIO14 triple-booking lesson, §5).

**Evidence tags** (used throughout the dossiers, keep the discipline):
`[CONFIRMED]` — stated in a service manual / verified by bench or multiple independent
sources · `[INFERRED]` — strong engineering inference, not explicitly documented ·
`[VERIFY]` — must be measured/read on the bench before committing copper. OCR-extracted
manual text stays `[VERIFY]` until eyeballed against the page image.

---

## 1. Canonical board shape

- **Module:** ESP32 WROOM-32 class (Wi-Fi, PCB antenna). No Ethernet.
- **Enclosure:** plastic (ABS/PETG — PETG near warm equipment); the PCB antenna points
  toward a case edge, never inside metal, mounted away from transformers/motors.
- **Power: deck-derived only** — no wall plugs, no USB, no PoE. Each deck powers its
  satellite from its own low-voltage rail (per-device tap in the dossier).
- **First flash over USB-serial is the only wired step in a board's life**; everything
  after ships OTA (dual-bank, verify-before-swap, rollback on non-validated image) — a
  power dip mid-flash must roll back, these boards are reachable only over Wi-Fi.

## 2. Power posture

- **Wi-Fi automatic light-sleep** (DTIM-driven wakes): average draw ≈ **15 mA** while
  staying associated and instantly commandable. Note the tension the research pass
  recorded: "reachable for OTA" costs more average current than "wake only to act" —
  rails are sized for the reachable-idle case, and the **sustained OTA download load**,
  not just command bursts.
- **Reservoir network on every tap** (light-sleep + reservoir are a pair):
  - **1000 µF low-ESR** across the tapped rail (low-ESR is load-bearing — it soaks the
    300–500 mA Wi-Fi TX spikes so the deck rail only sees the average),
  - **2.2–10 Ω inrush resistor** in series with the big cap (the deck rail must not see
    the cap-fill surge at power-up),
  - **100 µF + 0.1 µF** decoupling at the board.
- Rails rated ~150 mA get a **100–200 mA fuse on the tap** — a board fault must not be
  able to overdraw the host's rail (explicit on the A77's 27 V pin; apply the same
  thinking to every tap).

## 3. The ground-domain rule (safety)

Pick **ONE ground domain per board and commit.** A board powered from the host's
isolated secondary floats in that domain; the control driver into that same domain then
needn't be isolated, but **any other external galvanic connection must be**. The
OTA-after-install workflow is what makes this clean: the only earth-referenced
connection (USB programmer) exists **on the bench, before install**, and never coexists
with the board wired into the host; Wi-Fi is galvanically isolated by nature.

Per-device, before trusting any tap: **meter the candidate rail's ground against mains
earth and against chassis, power-off then power-on** — `[VERIFY]` on every unit, and the
*gating* decision on the Panasonic (see its dossier). Never probe an SMPS primary.

## 4. Output-stage philosophy

- **Never drive a host's signal node high.** Every control output is
  **open-collector / open-drain — pull low to assert, release to idle** (opto-isolated
  where the dossier says so). Two open-collector drivers on one node wire-OR safely.
- Contact-closure interfaces (A77) use **floating opto-MOSFET SSRs** (AQY212 / TLP222 /
  G3VM-61A1) across the host's own button pin-pairs — polarity-agnostic, isolated
  regardless of how the board is powered.
- Baseband-IR interfaces (Pioneer, Panasonic) replay the deck's own remote codes with
  the **38 kHz carrier stripped** (mark = pull low, space = release). The proven
  Wirenboard IR-blaster captures are the code ground truth — same data, carrier off.

## 5. ESP32 pin rules (re-audited 2026-07-12 against Espressif docs — DES-1)

Facts from the ESP32 Series Datasheet §Boot Configurations and the ESP32 hardware
design guidelines (schematic checklist):

- **Strapping pins: GPIO0, GPIO2, GPIO5, GPIO12 (MTDI), GPIO15 (MTDO).** Sampled at
  reset release, then freed as normal IO. Keep front-end loads off them entirely on
  these boards — a pulled strap means wrong flash voltage (GPIO12) or download mode
  (GPIO0/GPIO2). Free pins are plentiful; there is no reason to fight the straps.
- **GPIO34–39 are input-only** (no output driver, no internal pulls) — fine for sensor
  and status inputs (A77 motion, B215 status read-back), never for outputs.
- **GPIO14 is MTMS (JTAG TMS)** with a weak internal pull-up at reset — harmless into
  an opto LED behind a series resistor, but note it when an output must idle low.
- **The GPIO14 lesson (why this section exists):** the retired single-image firmware
  assigned GPIO14 in *three* drivers at once (A77 STOP, B215 LINK, shared IR out) —
  invisible in a runtime-identity image, a real conflict the moment anything shares a
  board or a harness. Under `per-device-apps` each board owns its pin map in its own
  app, and **every board's map gets audited against the strapping/IO-MUX tables at
  design time** (the mandatory DES-3 audit step). Legacy pin choices in the dossiers
  are `[INFERRED]` starting points, not commitments.

## 6. Command surface & safety conventions

- Per-device command surfaces (control names + momentary/stateful types) live in the
  dossiers; they are the raw material for the DES-4 descriptors (bridge
  device-integration-convention, `consumer-pins`).
- **Record arming:** any device exposing `record` requires an `arm_record` within a
  short window (legacy default 8 s), the arm consumed on use — a stray message must
  never start a recording over a tape. Bench-proven convention; keep it.
- Device-specific interlocks (A77 reel-motion, B215 never-drive-high) are in the
  dossiers and are **non-negotiable** parts of the device truth.

## 7. What this family is NOT

- No mains switching (the A77 has a hard power switch; automating mains is a separate,
  properly-rated relay project — explicitly out of scope).
- No IR carrier generation anywhere (both IR-path decks take baseband).
- No multi-device firmware image, ever (`per-device-apps`).

"""DES-8 — voice-satellite wall enclosure, Waveshare ESP32-S3-Touch-LCD-1.46B.

Parametric build123d source (v0 — geometry per docs/design/satellite_enclosure.md;
DES-9 iterates fit/acoustics on the printed part). Owner decisions 2026-07-18:
squircle body, straight-plug open bottom (variant B), bottom-only openings,
matte white PETG, keyhole wall mount.

Frame = the vendor STEP frame: origin at board centre, X right (front view),
Y up, Z toward the viewer's face; the wall is at negative Z. All mm.
Run:  ~/cad/build123d-env/bin/python case.py   → build/ STEP + STL per part.
"""

from dataclasses import dataclass
from pathlib import Path

from build123d import (
    Align, Axis, Box, BuildPart, BuildSketch, Circle, Cylinder, Location, Locations,
    Mode, Plane, Rectangle, RectangleRounded, export_step, export_stl, extrude,
    fillet, offset,
)

OUT = Path(__file__).parent / "build"


@dataclass(frozen=True)
class P:
    # measured board truth (STEP survey 2026-07-18; docs/design/satellite_enclosure.md §2)
    board_w: float = 39.36
    board_h: float = 41.53
    board_cy: float = -1.03          # board outline centre offset in Y
    face_z: float = -1.89            # display face plane
    board_back_z: float = -7.68      # PCB back face
    deepest_z: float = -12.95        # header pins — deepest metal
    view_d: float = 37.36            # viewing circle — lip stays OUTSIDE
    disp_cy: float = 0.0             # display centred on X/Y=0 (2D print front view)
    usb = (0.0, -19.20, 8.94, 7.60)  # cx, cy, w, h — bottom tab zone
    mic = (-14.20, -12.05)           # port on back face
    spk = (11.17, 0.00, 14.65, 10.0)  # cx, cy, w, h — soldered, rear-firing
    sw_y = (9.91, -10.20)            # side switches, actuators at +X edge
    sw_z: float = -8.10
    bosses = ((12.00, -14.95), (-11.54, -15.45), (0.00, 17.75))  # SMTSO-M2-3.5
    boss_top_z: float = -10.90       # standoff outer end (3.2 proud of back face)
    pillar_seat_z: float = -11.00    # pillar tops 0.1 SHY of the boss ends — the
    # (−11.54, −15.45) boss carries a collar 0.1 deeper than the surveyed −10.90
    # (full-STEP boolean, delta 8); the M2 preload closes the ≤0.2 gap at all three

    # case parameters
    clr: float = 0.45                # board-to-cavity clearance per side
    wall: float = 2.4
    bezel_t: float = 2.0             # front wall over the display edge
    lip_d: float = 38.2              # bezel opening (0.42 outside viewing circle)
    corner_r: float = 20.0
    back_in_z: float = -13.4         # cavity back plane (clears pins at -12.95)
    plate_t: float = 2.4
    keyhole_xy = ((-10.0, -6.0), (10.0, -6.0))  # metal kept low — antenna band is top
    mic_duct_w: float = 2.0
    spk_cavity_t: float = 3.2        # rib depth sealing to board back via foam gasket
    usb_slot_w: float = 11.0         # variant B open bottom for a straight plug
    usb_slot_d: float = 6.0
    pin_hole_d: float = 1.6          # switch service pinholes

    # retention (C-10): shell skirt to the wall + 2 M2 from below into plate feet
    # + 2 plastic teeth hooking plate-top rebates. Metal stays in the low band;
    # the teeth flank the top SMTSO screw head (x ±2.1) — a centred tooth would
    # land ON that head, and the antenna band gets plastic only.
    foot_x: float = 8.6              # screw axes at ±foot_x — clear of USB (±5.5) and slots (13.4+)
    foot_w: float = 4.6              # foot boss width (x) — pilot Ø1.7 keeps ≥1.1 wall
    screw_z: float = -11.4           # screw axis depth: foot spans z ±2.0 around it
    screw_clear_d: float = 2.3
    screw_pilot_d: float = 1.7
    tooth_x: float = 8.0             # tooth centres at ±tooth_x
    tooth_w: float = 4.0             # rebate is +0.3/side; tooth z 0.95 in a 1.25 rebate

    @property
    def cav_w(self): return self.board_w + 2 * self.clr
    @property
    def cav_h(self): return self.board_h + 2 * self.clr + 1.3  # + USB tab room at bottom
    @property
    def cav_cy(self): return self.board_cy - 0.65
    @property
    def out_w(self): return self.cav_w + 2 * self.wall
    @property
    def out_h(self): return self.cav_h + 2 * self.wall
    @property
    def front_z(self): return self.face_z + self.bezel_t
    @property
    def back_z(self): return self.back_in_z - self.plate_t


p = P()


def squircle(w, h, r):
    return RectangleRounded(w, h, min(r, w / 2 - .01, h / 2 - .01))


# ---------------------------------------------------------------- front shell
# Bezel + side walls; the skirt (C-10) runs past the plate to the wall plane, so
# the silhouette closes and the plate rim is captured with the 0.15 pocket gap.
with BuildPart() as front:
    with BuildSketch(Plane.XY.offset(p.back_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.out_w, p.out_h, p.corner_r)
    extrude(amount=p.front_z - p.back_z)
    # cavity + plate pocket (leaves the front bezel wall); the plate outline is
    # cav −0.3, so the same prism gives the skirt its 0.15/side rim clearance
    with BuildSketch(Plane.XY.offset(p.back_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.cav_w, p.cav_h, p.corner_r - p.wall)
    extrude(amount=(p.face_z - p.back_z), mode=Mode.SUBTRACT)
    # display opening through the bezel
    with BuildSketch(Plane.XY.offset(p.face_z)) as sk:
        with Locations((0, p.disp_cy)):
            Circle(radius=p.lip_d / 2)
    extrude(amount=p.bezel_t, mode=Mode.SUBTRACT)
    # bottom aperture: straight USB plug (variant B), centred under the connector
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.usb[0], p.cav_cy - p.out_h / 2, (p.face_z + p.back_in_z) / 2))):
            Box(p.usb_slot_w, 2 * p.wall + 2, p.usb_slot_d)
    # display FPC tail relief (delta 8): the touch/display film wraps the board's
    # bottom edge at x ≈ −6.7 and reaches y −23.12 — 0.1 past the cavity's corner
    # arc (−23.05 there). Local 0.4 pocket in the wall face; 2.0 wall remains.
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((-6.7, -23.15, -3.3))):
            Box(3.0, 0.6, 3.2)
    # switch service pinholes, right wall (actuators at +X)
    with BuildPart(mode=Mode.SUBTRACT):
        for y in p.sw_y:
            with Locations(Location((p.out_w / 2, y, p.sw_z), (0, 90, 0))):
                Cylinder(radius=p.pin_hole_d / 2, height=2 * p.wall + 2)
    # mic inlet: at the mic's X the bottom wall is the CORNER ARC band (y −22.2…−19.1,
    # not the rectangular −25.9) — the hole is drilled through that band and exits on
    # the under-curve.
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.mic[0], -20.6, p.back_in_z + 1.2), (90, 0, 0))):
            Cylinder(radius=0.9, height=8)
    # speaker grille: three slots through the bottom corner-arc band under the duct.
    # Cut boxes run LONG (y 10): the band migrates inboard with x (inner face at
    # y −19.1 by x 14.2) — a short box leaves the outermost slot blind (owner-caught).
    with BuildPart(mode=Mode.SUBTRACT):
        for dx in (-3.0, 0.0, 3.0):
            with Locations(Location((p.spk[0] + dx, -22.5, p.back_in_z + 1.2))):
                Box(1.6, 10.0, 2.6)
    # retention teeth (C-10): added AFTER the cuts so the pocket prism can't eat
    # them. Each tooth lives in the wall-side sliver z −15.65…−14.7 and laps the
    # plate-top edge arc (engagement 0.7…2.0 across its width); the box runs into
    # the skirt wall to bond and stays inside the outer wall (21.83 at x 10). The
    # tooth underside is a ~1–2 mm FDM micro-bridge on the face-down print.
    with BuildPart():
        for sx in (p.tooth_x, -p.tooth_x):
            with Locations(Location((sx, 19.05, -15.175))):
                Box(p.tooth_w, 2.9, 0.95)
    # retention screws: clearance bores up through the corner-arc band + spot-faces
    # flattening the under-curve for the pan heads. Bore top −22.0 stops shy of the
    # plate-foot face (the foot's pilot is the plate's own cut).
    with BuildPart(mode=Mode.SUBTRACT):
        for sx in (p.foot_x, -p.foot_x):
            with Locations(Location((sx, -24.0, p.screw_z), (90, 0, 0))):
                Cylinder(radius=p.screw_clear_d / 2, height=4.0)
            with Locations(Location((sx, -26.0, p.screw_z), (90, 0, 0))):
                Cylinder(radius=2.2, height=2.9)   # seat plane y −24.55, Ø4.4

# ---------------------------------------------------------------- back plate
# Closes the shell; carries keyholes, M2 screw holes into the board standoffs,
# the mic gasket ring + duct rib line, and the speaker cavity rib.
with BuildPart() as back:
    with BuildSketch(Plane.XY.offset(p.back_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.cav_w - 0.3, p.cav_h - 0.3, p.corner_r - p.wall)
    extrude(amount=p.plate_t)
    # M2 clearance holes + countersink seats at the measured standoff positions
    with BuildPart(mode=Mode.SUBTRACT):
        for (x, y) in p.bosses:
            with Locations(Location((x, y, p.back_z + p.plate_t / 2))):
                Cylinder(radius=1.15, height=p.plate_t + 2)
            with Locations(Location((x, y, p.back_z + 0.6))):
                Cylinder(radius=2.1, height=1.2)
    # standoff pillars: plate inner face up to the SMTSO boss ends. r 2.3: the top
    # boss (y 17.75) reaches 20.05 vs the cavity's 20.19 top — still > the SMTSO
    # flange Ø3.5 it seats.
    with BuildPart():
        for (x, y) in p.bosses:
            with Locations(Location((x, y, (p.back_in_z + p.pillar_seat_z) / 2))):
                Cylinder(radius=2.3, height=p.back_in_z * -1 + p.pillar_seat_z)
    # mic gasket ring: seals against the MIC CAN'S ported face (NOT the board — the can
    # sits 0.9 proud, Z -8.60; a board-plane ring would crash into it). Ring lands fully
    # on the 4.7 x 5.0 can (outer Ø4.4), stops 0.5 shy for the gasket washer's crush
    # (adhesive foam/silicone, ~Ø4.5 x 0.8 -> 0.5 compressed, bore ~Ø1.5 over the port).
    with BuildPart():
        mic_face_z = -8.60
        ring_h = -(p.back_in_z - mic_face_z) - 0.5
        with Locations(Location((p.mic[0], p.mic[1], p.back_in_z + ring_h / 2))):
            Cylinder(radius=2.2, height=ring_h)
        duct_l = abs((p.cav_cy - p.cav_h / 2) - p.mic[1])
        for dx in (-p.mic_duct_w / 2 - 0.6, p.mic_duct_w / 2 + 0.6):
            with Locations(Location((p.mic[0] + dx, p.mic[1] - duct_l / 2, p.back_in_z + 1.0))):
                Box(1.2, duct_l, 2.0)
        # roof over the rail channel → a CLOSED tunnel (owner question 2026-07-19:
        # isolation — one defined path instead of coupling the mic to the case cavity;
        # the 2 mm bridge span is trivial FDM). Clipped at the rim by the outline
        # prism; the rim hand-off pocket to the shell inlet stays a DES-9 gasket item.
        # Top −11.05, sunk 0.25 into the rail tops (delta 8): the (−11.54, −15.45)
        # SMTSO body reaches −10.90 over the duct's east rail line — the delta-7
        # slab (top −10.8) clipped it 0.1; 0.15 clearance now, tunnel still closed.
        with Locations(Location((p.mic[0], p.mic[1] - duct_l / 2, -11.35))):
            Box(4.4, duct_l, 0.6)
    # the acoustic L inside the ring (owner-caught: the v0 bore dead-ended DOWN into
    # the plate slab while the duct channel hit the ring's solid side — no through
    # path). Bore now stops at channel height; a side passage exits south through the
    # ring wall into the rail channel.
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.mic[0], p.mic[1], -10.8))):
            Cylinder(radius=0.9, height=4.6)   # bore -8.5..-13.1: gasket face → channel level
        with Locations(Location((p.mic[0], p.mic[1] - 1.9, -12.55))):
            Box(1.8, 4.0, 1.7)                 # side passage through the ring wall
    # speaker cavity rib box (seals around the soldered speaker). The speaker's right
    # edge is 1.2 from the board edge, so the box is ASYMMETRIC: right rib squeezed to
    # the plate rim (outer face at 19.85, inside the 19.98 rim), the rest roomy.
    with BuildPart():
        rib_h = -(p.back_in_z - p.board_back_z) - 0.5
        sx, sy, sw, sh = p.spk
        rib = 1.2
        x0, x1 = sx - sw / 2 - 2.0, 19.85          # inner-left bound, outer-right limit
        y0, y1 = sy - sh / 2 - 2.0, sy + sh / 2 + 2.0
        zc = p.back_in_z + rib_h / 2
        with Locations(Location(((x0 - rib + x1) / 2, y1 + rib / 2, zc))):
            Box(x1 - x0 + rib, rib, rib_h)          # top — flush right at x1
        with Locations(Location(((x0 - rib + x1) / 2, y0 - rib / 2, zc))):
            Box(x1 - x0 + rib, rib, rib_h)          # bottom — flush right at x1
        with Locations(Location((x0 - rib / 2, sy, zc))):
            Box(rib, y1 - y0 + 2 * rib, rib_h)      # left
        with Locations(Location((x1 - rib / 2, sy, zc))):
            Box(rib, y1 - y0 + 2 * rib, rib_h)      # right — flush at the rim limit
    # duct opening: gap in the bottom rib toward the grille slots — OFFSET LEFT to
    # x 7.5: the lower-right SMTSO pillar (12.00, -14.95, r 2.3 → x 9.7..14.3) sits
    # dead on the centred path (probe-caught); the primary sound line now runs clear
    # of it. DES-9's sealed duct must skirt the pillar likewise.
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((7.5, p.spk[1] - p.spk[3] / 2 - 2.0 - 0.6, p.back_in_z + 1.4))):
            Box(5.0, 3.0, 2.4)
    # rib clearance notches (delta 8): the full-STEP boolean found back-side parts
    # CROSSING the rib lines — the 0.5 gasket gap assumed a bare board back. Ribs
    # are notched around them (+0.4 clearance); sealing over the notches is a DES-9
    # gasket item (thicker foam strips at the notch floors).
    with BuildPart(mode=Mode.SUBTRACT):
        # battery connector (x 0.7…5.7, proud to −9.2) + tinies — left rib
        with Locations(Location((3.45, 0.8, -8.8))):
            Box(6.3, 7.0, 1.6)
        # small parts to −8.4/−8.5 — bottom-rib west run
        with Locations(Location((3.4, -7.0, -8.4))):
            Box(6.4, 3.4, 0.8)
        # part to −8.42 — top-rib west end
        with Locations(Location((1.45, 7.35, -8.4))):
            Box(2.5, 2.7, 0.8)
        # switch bodies (proud to −9.2) — top/bottom rib east corners
        with Locations(Location((14.85, 7.85, -8.8))):
            Box(2.5, 1.7, 1.6)
        with Locations(Location((14.85, -8.0, -8.8))):
            Box(2.5, 1.4, 1.6)
    # retention feet (C-10): bosses the two from-below screws thread into. Boxes run
    # deliberately past the bottom edge (−22.6) so the global outline intersect trims
    # their underside to the plate's corner arc — which lands them 0.24…0.28 above
    # the skirt band's cavity face. z −13.4…−9.4 stays 1.7 behind the PCB back; plan
    # position clears USB (x ±4.47), the mic duct rails (−16.4…−12.0) and the
    # lower-right SMTSO pillar (x 9.7…14.3 at y ≥ −17.25) — STEP-verified.
    with BuildPart():
        for sx in (p.foot_x, -p.foot_x):
            with Locations(Location((sx, -20.25, p.screw_z))):
                Box(p.foot_w, 4.7, 4.0)
    # assembly-fit rule: clip EVERYTHING (ribs, rails, pillars) to the plate outline —
    # the squircle corner arcs narrow the cavity; features placed by rectangle math
    # (spk box corner, mic duct rails) are trimmed here instead of per-feature.
    with BuildSketch(Plane.XY.offset(p.back_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.cav_w - 0.3, p.cav_h - 0.3, p.corner_r - p.wall)
    extrude(amount=10, mode=Mode.INTERSECT)  # generous height — covers every feature top
    # keyhole slots (screw head Ø7 entry, Ø3.6 slide-up), metal low, clear of antenna
    with BuildPart(mode=Mode.SUBTRACT):
        for (x, y) in p.keyhole_xy:
            with Locations(Location((x, y, p.back_z + p.plate_t / 2))):
                Cylinder(radius=3.6, height=p.plate_t + 2)
            with Locations(Location((x, y + 5.0, p.back_z + p.plate_t / 2))):
                Box(3.7, 10.0, p.plate_t + 2)
    # retention rebates + pilots (C-10). Rebates: the top-edge BACK corner is
    # relieved (z −15.8…−14.55) so the shell teeth sit between wall and the
    # remaining front-layer ledge — shell creep (+Z) presses tooth on ledge.
    # Flanks the top SMTSO countersink head (x ±2.1) — never cut near it.
    # Pilots: Ø1.7 up into the feet, floor 0.4 under the foot top (M2 forms
    # ~3.8 mm of thread from the arc face).
    with BuildPart(mode=Mode.SUBTRACT):
        for sx in (p.tooth_x, -p.tooth_x):
            with Locations(Location((sx, 18.9, -15.175))):
                Box(p.tooth_w + 0.6, 3.2, 1.25)
        for sx in (p.foot_x, -p.foot_x):
            with Locations(Location((sx, -20.5, p.screw_z), (90, 0, 0))):
                Cylinder(radius=p.screw_pilot_d / 2, height=4.4)

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, part in (("front-shell", front.part), ("back-plate", back.part)):
        export_step(part, str(OUT / f"{name}.step"))
        export_stl(part, str(OUT / f"{name}.stl"))
        bb = part.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, "
              f"volume {part.volume / 1000:.1f} cm3")
    print(f"case footprint {p.out_w:.1f} x {p.out_h:.1f}, depth off wall "
          f"{p.front_z - p.back_z:.1f} mm")

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
# Bezel + side walls; open at the back where the plate closes it.
with BuildPart() as front:
    with BuildSketch(Plane.XY.offset(p.back_in_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.out_w, p.out_h, p.corner_r)
    extrude(amount=p.front_z - p.back_in_z)
    # cavity (leaves the front bezel wall)
    with BuildSketch(Plane.XY.offset(p.back_in_z)) as sk:
        with Locations((0, p.cav_cy)):
            squircle(p.cav_w, p.cav_h, p.corner_r - p.wall)
    extrude(amount=(p.face_z - p.back_in_z), mode=Mode.SUBTRACT)
    # display opening through the bezel
    with BuildSketch(Plane.XY.offset(p.face_z)) as sk:
        with Locations((0, p.disp_cy)):
            Circle(radius=p.lip_d / 2)
    extrude(amount=p.bezel_t, mode=Mode.SUBTRACT)
    # bottom aperture: straight USB plug (variant B), centred under the connector
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.usb[0], p.cav_cy - p.out_h / 2, (p.face_z + p.back_in_z) / 2))):
            Box(p.usb_slot_w, 2 * p.wall + 2, p.usb_slot_d)
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
            with Locations(Location((x, y, (p.back_in_z + p.boss_top_z) / 2))):
                Cylinder(radius=2.3, height=p.back_in_z * -1 + p.boss_top_z)
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
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.mic[0], p.mic[1], p.back_in_z + 2))):
            Cylinder(radius=0.9, height=8)  # port bore through the ring
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
    # duct opening: gap in the bottom rib toward the grille slots
    with BuildPart(mode=Mode.SUBTRACT):
        with Locations(Location((p.spk[0], p.spk[1] - p.spk[3] / 2 - 2.0 - 0.6, p.back_in_z + 1.4))):
            Box(6.0, 3.0, 2.4)
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

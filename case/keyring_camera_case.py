#!/usr/bin/env python3
"""
Keyring snapshot camera (ESP32-S3, 10-unit gift run) - parametric case, two variants:
  BMO-style  : rounded-rect body, landscape screen as the "face" w/ raised bezel,
               camera ring top-left, 4-key diamond keypad lower-right, post top-right.
  Mini-camera: classic Y2K keyring cam face plate, lens ring top centre w/ proud ring,
               flash/viewfinder recess top-right, screen below, decorative plate, post top-left.

Run:  .venv/bin/python keyring_camera_case.py
Out:  bmo_body.stl, bmo_back.stl, camera_body.stl, camera_back.stl (+ STEP + PNG previews)

Build coordinate system (all mm):
  X across the 25 mm PCB dimension, Y up the device (battery runs along Y), Z = thickness.
  Origin at case centre in X/Y, z=0 at the REAR outer face (lid floor outer surface).

Z stack (bottom -> top):
  lid floor            0.0 -  1.2
  battery (401230)     1.2 -  4.4   (behind the PCB plane, x -11.9..0.1, full bay length)
  speaker (15x11x4)    1.2 -  5.2   (flat on the lid floor beside the battery, x 0.6..11.6,
                                    y -20.4..-5.4, faces DOWN through the rear grille)
  rear grille          4 slots through the lid floor, x 1.6..11.6
  PCB shelf lip        3.8 -  4.6   (front shell inner lip; PCB nubs at the bottom edge)
  main PCB             4.6 -  5.4   (25 x 26 x 0.8)
  snap hooks (lid)     catch under the lip at z 3.4..3.8
  display FPC fold     5.4 -  6.9
  display module       6.9 -  8.9   (glass top; front inner wall at 9.3 -> 0.4 clearance)
  front wall           9.3 - 10.6   (face plate)
  keypad FPC board     8.7 -  9.3   (BMO only, bonded to inner face; buttons hang to 6.7)
  camera board         5.4 -  6.4, lens barrel nose to z 12.4 (through Ø6.4 front hole)
  lens ring (proud)    10.6 - 11.8
USB-C mouth: through the TOP (-Y is bottom here) wall, i.e. the short 1.2 mm wall
  behind the PCB's opposite edge - connector sits right behind the wall, no corridor.
Total assembled thickness: 12.4 mm <= 14 mm target.

NOTE on footprint: the brief asks for ~25 x 26 x 12, but the hard 401230 battery
(40x12x3.2) physically cannot fit behind a 25x26 PCB. The case therefore grows along
Y to 44.2 mm outer (29.6 x 45.8 with lid skirt) - see BATT_LEN. Set BATT_STUB=True
and the parametric script collapses the lower bay for a 20x20x3.5 cell (not built by
default; PCB openings/positions would need re-tuning).
"""

import math
import os

from build123d import (
    Align, Axis, Box, Circle, Cylinder, Location, Pos, RectangleRounded,
    Rectangle, Rot, extrude, export_stl, export_step,
)

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# HARD COMPONENT DIMENSIONS (drive every opening)
# ----------------------------------------------------------------------------
PCB_W, PCB_H, PCB_T = 25.0, 26.0, 0.8          # 25 x 26 x 0.8, corners R2
LCD_W, LCD_H, LCD_T = 22.5, 14.5, 2.0          # display module PCB footprint
LCD_GLASS_W, LCD_GLASS_H = 21.7, 10.8          # active glass area
CAM_BARREL_L = 6.0                             # barrel above camera board
CAM_APER_D = 5.5                               # lens aperture
CAM_FLANGE_D = 8.0                             # barrel flange
BATT_W, BATT_L, BATT_H = 12.0, 40.0, 3.2       # 401230 LiPo
BATT_STUB = False                              # True -> 20x20x3.5 cell, shorter case
SPK_W, SPK_H, SPK_T = 15.0, 11.0, 4.0          # speaker
USB_MOUTH_W, USB_MOUTH_H = 9.4, 3.6            # 8.94x3.26 + FDM clearance
TF_SLOT_H = 12.0                               # slot mouth height
TF_CARD_OVERHANG = 3.5                         # card poke-out
BTN_SIDE_W = 3.6                               # side button opening (6x6 tactile)
POST_BORE = 6.2                                # fits 6 mm steel split ring
POST_OD = 10.0                                 # ~1.9 mm section

# ----------------------------------------------------------------------------
# CASE / PRINT PARAMETERS (tuned for FDM, 0.15-0.25 mm clearance, 2-perimeter walls)
# ----------------------------------------------------------------------------
WALL = 1.2                                     # >= 2-perimeter (0.8) everywhere
CLS = 0.25                                     # general clearance, openings
PCB_CLS = 0.3                                  # PCB pocket clearance
CHAM = 0.4                                     # edge chamfer
FRONT_T = 10.6                                 # case total Z at face
CAV_DEPTH = 9.3                                # cavity inner front plane
LID_T = 1.2                                    # rear floor
SKIRT_H = 5.8                                  # lid skirt wrap height
SKIRT_T = 0.8                                  # lid skirt thickness (2 perimeters)
CR_OUT, CR_IN = 4.5, 3.3                       # outer / inner corner radius

# battery bay
BAY_X0, BAY_X1 = -12.4, 0.3                    # battery sits here (guide rails outside)
BAY_Y0, BAY_Y1 = -20.5, 19.5                   # 41 mm of bay for the 40 mm cell
BATT_X0, BATT_X1 = -11.9, -11.9 + BATT_W       # -11.9 .. 0.1

# speaker (assembly only - lies flat on the lid floor, faces DOWN through the grille)
SPK_X0, SPK_X1 = 0.6, 11.6                     # x span 11 mm, beside the battery
SPK_Y0, SPK_Y1 = -20.4, -5.4                   # y span 15 mm, clear of the PCB edge
SPK_Z0, SPK_Z1 = 1.2, 5.2                      # 4 mm body on the lid floor
GRILLE = ((1.6, 3.2), (4.4, 6.0), (7.2, 8.8), (10.0, 11.6))   # rear grille slots, x spans
GRILLE_Y0, GRILLE_Y1 = -19.4, -11.4            # slot length 8 mm in y

# perimeter / interconnect (both variants)
PCB_Z0, PCB_Z1 = 4.6, 5.4                      # PCB plane
USB_Z = 5.4                                    # connector mid z
USB_Z0, USB_Z1 = USB_Z - USB_MOUTH_H / 2 - 0.2, USB_Z + USB_MOUTH_H / 2 + 0.2
TF_Y0, TF_Y1 = -3.6, 8.4                       # slot mouth on right wall (PCB right edge)
TF_Z0, TF_Z1 = 3.9, 7.3
SHUTTER_Y, FUNC_Y = 10.4, 10.9                 # side tactile button centres
SIDE_Z0, SIDE_Z1 = 4.2, 6.6
HOOK_YS = (2.5, 15.0)                          # lid snap hook rows

# keypad (BMO): 4-key diamond, SMD 3.5x3.5 tactiles on a bonded FPC keypad board
KEY_D = 4.4
KEYS = ((6.2, -9.6), (3.0, -13.1), (9.4, -13.1), (6.2, -16.6))  # up/left/right/down
KBD_T = 0.6                                    # keypad FPC board thickness
KBD_Z1 = 9.3                                   # board sits against the inner face

# ----------------------------------------------------------------------------
# VARIANT DEFINITIONS
# ----------------------------------------------------------------------------
VARIANTS = {
    "bmo": dict(
        lens=(-7.4, 13.8), ring_od=10.0, ring_proud=1.2,
        win=(-1.0, 1.0), frame_od=(22.8, 12.2), frame_id=(20.0, 9.4),
        frame_r=3.0, frame_proud=0.8,
        keypad=True, usb_cx=-0.5, post=(10.0, 19.8), plate=None, viewfinder=None,
    ),
    "camera": dict(
        lens=(-0.8, 12.8), ring_od=10.5, ring_proud=1.2,
        win=(-1.0, -0.4), frame_od=(21.6, 11.0), frame_id=(20.2, 9.6),
        frame_r=2.0, frame_proud=0.5,
        keypad=False, usb_cx=6.5, post=(-10.0, 19.8),
        plate=(-1.0, -13.0, 22.0, 12.5), viewfinder=(9.7, 13.4, 4.6, 4.0),
    ),
}

if BATT_STUB:
    raise SystemExit("BATT_STUB layout not wired: set BATT_STUB=False or port the "
                     "short-bay variant before running (documented in the docstring).")

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def rrect_prism(w, h, r, z0, z1, cx=0.0, cy=0.0):
    """Rounded-rect prism from z0 to z1 centred on (cx, cy)."""
    return Pos(cx, cy, z0) * extrude(RectangleRounded(w, h, r), z1 - z0)


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * \
        Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def cyl(x, y, z0, z1, r):
    return Pos(x, y, z0) * Cylinder(r, z1 - z0,
                                    align=(Align.CENTER, Align.CENTER, Align.MIN))


def rrect_hole(w, h, r, z0, z1, cx=0.0, cy=0.0):
    return rrect_prism(w, h, r, z0, z1, cx, cy)


def reduce_union(parts):
    out = None
    for p in parts:
        out = p if out is None else out + p
    return out


def reduce_cut(base, cuts):
    for c in cuts:
        base = base - c
    return base


# ----------------------------------------------------------------------------
# SHARED CUTTERS (applied to both shells where they overlap)
# ----------------------------------------------------------------------------
def shared_cutters(usb_cx):
    cuts = []
    # USB-C mouth through the TOP (+Y) wall (and the lip's top band there):
    # the connector sits right behind the 1.2 mm wall, so no plug corridor exists.
    halves = USB_MOUTH_W / 2
    cuts.append(box(usb_cx - halves, usb_cx + halves, 19.9, 23.3, USB_Z0, USB_Z1))
    # TF card slot mouth through the right (+X) wall only (starts at the cavity
    # wall so the lip rail under the PCB edge stays intact; card exits above it)
    cuts.append(box(12.6, 16.0, TF_Y0, TF_Y1, TF_Z0, TF_Z1))
    # speaker grille: 4 slots through the lid floor (rear face), under the speaker
    for x0, x1 in GRILLE:
        cuts.append(box(x0, x1, GRILLE_Y0, GRILLE_Y1, -0.1, LID_T + 0.05))
    # side button openings (+ proud finger dimples handled per shell)
    for y in (SHUTTER_Y, FUNC_Y):
        side = -1 if y == SHUTTER_Y else 1
        cuts.append(box(side * 16.0, side * 12.6, y - BTN_SIDE_W / 2,
                        y + BTN_SIDE_W / 2, SIDE_Z0, SIDE_Z1))
        cuts.append(cyl(side * 14.2, y, FRONT_T - 0.55, FRONT_T + 0.6, 2.75))
    return cuts


# ----------------------------------------------------------------------------
# FRONT SHELL (body) PER VARIANT
# ----------------------------------------------------------------------------
def build_front(v):
    cuts = shared_cutters(v["usb_cx"])
    adds = []

    # screen window + raised frame (bezel)
    wx, wy = v["win"]
    cuts.append(rrect_prism(19.6, 9.0, 1.8, 8.0, FRONT_T + 1.0, wx, wy))
    ring = (rrect_prism(v["frame_od"][0], v["frame_od"][1], v["frame_r"],
                        FRONT_T, FRONT_T + v["frame_proud"], wx, wy)
            - rrect_prism(v["frame_id"][0], v["frame_id"][1], v["frame_r"] - 0.6,
                          FRONT_T - 0.05, FRONT_T + v["frame_proud"] + 0.1, wx, wy))
    adds.append(ring)

    # camera hole + proud lens ring
    lx, ly = v["lens"]
    cuts.append(cyl(lx, ly, 8.0, FRONT_T + v["ring_proud"] + 1.0,
                    (CAM_APER_D + 0.9) / 2))
    adds.append(cyl(lx, ly, FRONT_T - 0.4, FRONT_T + v["ring_proud"], v["ring_od"] / 2)
                - cyl(lx, ly, FRONT_T - 0.5, FRONT_T + v["ring_proud"] + 0.1,
                      (CAM_APER_D + 0.9) / 2))

    # inner lip shelf that carries the PCB (continuous, z 3.8..4.6)
    lip = (rrect_prism(26.0, 42.2, 3.4, 3.8, 4.6)
           - rrect_prism(23.8, 40.0, CR_IN - 0.9, 3.7, 4.7))
    adds.append(lip)

    if v["keypad"]:
        # key holes only: the keypad FPC board is a separate part bonded to the
        # inner face (board 8.7..9.3, buttons hang to 6.7 in the open cavity)
        for kx, ky in KEYS:
            cuts.append(cyl(kx, ky, 8.0, FRONT_T + 0.8, KEY_D / 2))

    if v["viewfinder"]:
        fx, fy, fw, fh = v["viewfinder"]
        cuts.append(box(fx - fw / 2, fx + fw / 2, fy - fh / 2, fy + fh / 2,
                        FRONT_T - 1.0, FRONT_T + 0.6))

    if v["plate"]:
        px, py, pw, ph = v["plate"]
        adds.append(rrect_prism(pw, ph, 1.5, FRONT_T, FRONT_T + 0.5, px, py))
        for gy in (py - 3.5, py + 3.5):
            cuts.append(box(px - 8.0, px + 8.0, gy - 0.4, gy + 0.4,
                            FRONT_T + 0.28, FRONT_T + 0.6))

    front = rrect_prism(28.0, 44.2, CR_OUT, 0.0, FRONT_T) \
        - rrect_prism(25.6, 41.8, CR_IN, 0.0, CAV_DEPTH)

    front = reduce_union([front] + adds) if adds else front
    front = reduce_cut(front, cuts)

    # decorative keyring post tube (integral, through-height, bore for 6 mm ring)
    px, py = v["post"]
    post = cyl(px, py, 0.0, FRONT_T + 0.4, POST_OD / 2) - cyl(
        px, py, -0.2, FRONT_T + 0.5, POST_BORE / 2)
    front = front + post

    # chamfer the face-plate top rim (all top edges, 0.4) - best effort
    try:
        rim = [e for e in front.edges()
               if abs(e.center().Z - FRONT_T) < 0.01
               and max(abs(e.center().X), abs(e.center().Y)) > 12.0]
        try:
            front = front.chamfer(0.2, 0.2, edge_list=rim)
        except Exception:
            pass
    except Exception as e:  # noqa: BLE001
        print(f"  (face chamfer skipped: {type(e).__name__}: {e})")
    return front


# ----------------------------------------------------------------------------
# LID / BACK SHELL PER VARIANT
# ----------------------------------------------------------------------------
def build_back(v):
    cuts = shared_cutters(v["usb_cx"])
    adds = []

    # battery guide rails
    for rx0, rx1 in ((BAY_X0, BAY_X0 + 0.4), (BAY_X1 - 0.4, BAY_X1)):
        adds.append(box(rx0, rx1, BAY_Y0, BAY_Y1, LID_T - 0.2, 2.4))

    # PCB bottom-edge supports: thin risers from the lid floor up to the PCB plane,
    # outside the battery (x <= 0.3), speaker (x >= 0.6 ends at y -5.4) and USB mouth
    adds.append(box(0.5, 2.3, -5.2, -4.95, LID_T - 0.2, PCB_Z0))
    adds.append(box(11.8, 12.6, -5.2, -4.95, LID_T - 0.2, PCB_Z0))

    # snap hooks: cantilever risers catching under the front shell inner lip
    hx = 10.8
    for y in HOOK_YS:
        for sx in (1, -1):
            x = sx * hx
            adds.append(box(x - 0.6, x + 0.6, y - 3.0, y + 3.0,
                            LID_T - 0.2, 3.5))                   # riser
            adds.append(box(x - 0.2, sx * 12.2, y - 3.0, y + 3.0,
                            3.4, 3.8))                           # catch foot

    lid = rrect_prism(28.0, 44.2, CR_OUT, 0.0, LID_T)
    skirt = rrect_prism(29.6, 45.8, CR_OUT + 0.8, 0.0, SKIRT_H) \
        - rrect_prism(27.8, 44.0, CR_OUT - 0.2, -0.1, SKIRT_H + 0.1)
    lid = lid + skirt
    lid = reduce_union([lid] + adds) if adds else lid

    # relief slots in the skirt so the hook risk stays flex-free is not needed,
    # but keep the skirt breathable: nothing to cut here.
    lid = reduce_cut(lid, cuts)

    # clearance bore where the case's keyring post stands on the lid
    px, py = v["post"]
    lid = lid - cyl(px, py, -0.2, LID_T + 0.1, POST_OD / 2 + 0.15)

    try:
        bot_rim = [e for e in lid.edges()
                   if abs(e.center().Z) < 0.01
                   and max(abs(e.center().X), abs(e.center().Y)) > 13.5]
        lid = lid.chamfer(0.3, 0.3, edge_list=bot_rim)
    except Exception as e:  # noqa: BLE001
        print(f"  (lid chamfer skipped: {type(e).__name__}: {e})")
    return lid


# ----------------------------------------------------------------------------
# BUILD + VALIDATE + EXPORT
# ----------------------------------------------------------------------------
def validate(stl_path, name):
    import trimesh
    m = trimesh.load(stl_path, force="mesh")
    vol = m.volume
    ok = m.is_watertight and vol > 0
    print(f"  {name}: faces={len(m.faces)}, watertight={m.is_watertight}, "
          f"volume={vol:.1f} mm^3, bbox={m.bounds[1] - m.bounds[0]}")
    return ok


def render(stl_path, png_path, title):
    import trimesh
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    m = trimesh.load(stl_path, force="mesh")
    tris = m.vertices[m.faces]
    n = m.face_normals
    light = np.array([0.4, 0.35, 0.85])
    light = light / np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(-(n @ light) * 0 + (n @ np.array([0.3, 0.4, 0.87])), 0, 1)
    col = plt.cm.Greys(0.25 + 0.6 * shade)

    fig = plt.figure(figsize=(5, 6))
    ax = fig.add_subplot(111, projection="3d")
    pc = Poly3DCollection(tris, facecolors=col, edgecolors="none")
    ax.add_collection3d(pc)
    b = m.bounds
    c, r = (b[0] + b[1]) / 2, (b[1] - b[0]).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=18, azim=-60)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(png_path, dpi=110)
    plt.close(fig)
    print(f"  rendered {os.path.basename(png_path)}")


def main():
    all_ok = True
    for key, v in VARIANTS.items():
        print(f"[{key}] building...")
        front = build_front(v)
        back = build_back(v)
        stl_f = os.path.join(HERE, f"{key}_body.stl")
        stl_b = os.path.join(HERE, f"{key}_back.stl")
        export_stl(front, stl_f)
        export_stl(back, stl_b)
        try:
            export_step(front, os.path.join(HERE, f"{key}_body.step"))
            export_step(back, os.path.join(HERE, f"{key}_back.step"))
        except Exception as e:  # noqa: BLE001
            print(f"  STEP export failed: {e}")
        all_ok &= validate(stl_f, f"{key}_body")
        all_ok &= validate(stl_b, f"{key}_back")
        try:
            render(stl_f, os.path.join(HERE, f"{key}_body.png"), f"{key} - body (front)")
            render(stl_b, os.path.join(HERE, f"{key}_back.png"), f"{key} - back shell")
        except Exception as e:  # noqa: BLE001
            print(f"  render failed ({type(e).__name__}: {e}) - moving on")
        print(f"[{key}] front solids: {len(front.solids())}, "
              f"back solids: {len(back.solids())}")
        for tag, part in (("front", front), ("back", back)):
            for s in part.solids():
                if s.volume < 1.0:
                    b = s.bounding_box()
                    print(f"  SLIVER in {key} {tag}: vol={s.volume:.3f} "
                          f"min={b.min} max={b.max}")
    print("ALL WATERTIGHT OK" if all_ok else "WARNING: non-manifold part detected")


if __name__ == "__main__":
    main()

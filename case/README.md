# 3D-printed case — two variants

Parametric shell for the keyring camera (28 × 44.2 × 12.4mm assembled). Generated with build123d; all four STLs re-imported and validated watertight by `keyring_camera_case.py` on export.

- **BMO-style** (`bmo_*`): screen-face BMO bezel, camera aperture as a corner "eye", **4-key diamond game pad**, keyring post top-right
- **Mini-camera** (`camera_*`): centre-top lens ring + proud ring, flash/viewfinder recess, engraved two-tone face plate, no keypad

## Files

- `keyring_camera_case.py` — parametric source. **Every opening/dimension is a named variable at the top**; re-tune when real samples arrive (display glass proud-height, FPC fold gap, camera barrel vs ring, snap clearance).
- `stl/*.stl` — printable parts (bmo/back, camera/back, each variant: body = front, back = lid)
- `step/*.step` — editable solids
- `previews/*.png` — quick verification renders (grey matplotlib, not beauty shots)

## Print settings (PLA)

| Setting | Value |
|---|---|
| Orientation | face plate DOWN on the bed (bezel/rings/keyholes/post print self-supporting upward); lid outer face down; **no supports anywhere** |
| Layer | 0.16mm (0.12 for the final gift run) |
| Perimeters | 3–4 (walls ≥1.2mm) |
| Infill | 15% gyroid |
| Extras | brim on the keyring-post corner; ironing on the face for the toy look |
| Two-tone | mid-print filament swap (BMO: green body + pale bezel; mini-cam: cream + red shutter dimple); fuzzy-skin on the mini-cam plate if your printer supports it |

## Assembly

Snap-fit: front shell's inner lip carries the PCB; lid has 4 cantilever hooks (0.2mm clearance) that click under it. Battery glued on the lid floor rails; speaker beside it firing down through the lid grille. Keyring post takes a standard 6mm steel split ring. MicroSD pulls out through the open slot — no door. 0.15–0.25mm FDM clearances throughout.

**Print a first article at nominal clearance and test the hook engagement before the batch.**

## Rebuild

```
python3 -m venv .venv            # once
.venv/bin/pip install -r requirements.txt    # once
.venv/bin/python -I keyring_camera_case.py   # regenerates STL + STEP
```

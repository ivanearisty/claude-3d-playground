# Corner Lamp/Plant Shelf — Print & Assembly Notes

## Lamp
- OuXean Small Wood Table Lamp (open Edison bulb, dimmable)
- Base: 109 x 109 x 79mm (4.3" x 4.3" x 3.1")
- Weight: ~350g (0.77 lbs)
- Inline rotary dimmer, standard E26 socket

## Design
- Two-level corner shelf (90-degree wall corner)
- Upper: 170mm radius quarter circle (lamp) — cable crescent at corner
- Lower: 170mm radius quarter circle (plant)
- Arch brackets: smooth curved L-shape, screws at the bottom
- All pieces fit as single prints on A1 Mini (180mm bed)

## Print List

| File | Qty | Size | Notes |
|---|---|---|---|
| `upper_shelf.stl` | 1 | 170x170x14mm | Cable slot at corner |
| `lower_shelf.stl` | 1 | 170x170x14mm | No cable slot |
| `arch_bracket_x4.stl` | 4 | 50x50x25mm | 2 per level, 1 per wall |

**Total: 6 prints**

## Print Settings
- **Printer**: Bambu A1 Mini (180x180mm)
- **Material**: PLA or PETG
- **Layer height**: 0.2mm
- **Infill**: 30-40% (shelves), 50%+ (brackets — structural)
- **Walls**: 3-4 perimeters
- **Supports**: None needed
- **Orientation**: All pieces print flat

## Assembly

1. **Mount brackets** to walls with #8 wood screws
   - 2 brackets per shelf level (1 per wall)
   - Position ~40mm from the corner along each wall
   - Screw holes are at the bottom of the bracket (near the wall)
   - Use wall anchors if not hitting studs
2. **Place shelves** on brackets — shelf rests on the horizontal top face of each arch bracket
3. **Route lamp cord** through the cable crescent at the upper shelf corner and down the wall

## Hardware
- 8x #8 wood screws (4mm, 25-30mm long)
- 8x wall anchors (if needed)

## Adjusting Dimensions
Edit `params.json` and re-run `design.py`:
- `upper_radius_mm` / `lower_radius_mm`: shelf size (keep ≤ 180 for single-piece prints)
- `cable_slot_radius_mm`: 10mm fits most lamp cords
- `bracket_depth_mm` / `bracket_height_mm`: how far the bracket extends from the wall
- `bracket_thickness_mm`: wall thickness of the bracket arch (8mm default)

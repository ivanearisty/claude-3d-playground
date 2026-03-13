# Corner Lamp/Plant Shelf — Print & Assembly Notes

## Lamp
- OuXean Small Wood Table Lamp (open Edison bulb, dimmable)
- Base: 109 x 109 x 79mm (4.3" x 4.3" x 3.1")
- Weight: ~350g (0.77 lbs)
- Inline rotary dimmer, standard E26 socket

## Design
- Two-level corner shelf (90-degree wall corner)
- Both shelves: 170mm radius quarter circle, single piece on A1 Mini
- Upper shelf has cable crescent at corner for lamp cord
- Convex arch brackets: smooth taper from 60mm (shelf support) to 15mm (wall mount)
- Screw boss on wall face (raised pad for screw head clamping)
- **4 prints total**

## Print List

| File | Qty | Size | Notes |
|---|---|---|---|
| `upper_shelf.stl` | 1 | 170x170x14mm | Cable slot at corner |
| `lower_shelf.stl` | 1 | 170x170x14mm | No cable slot |
| `arch_bracket_x2.stl` | 2 | 65x80x25mm | 1 per shelf level |

## Print Settings
- **Printer**: Bambu A1 Mini (180x180mm)
- **Material**: PLA or PETG
- **Layer height**: 0.2mm
- **Infill**: 30% (shelves), 50%+ (brackets — structural)
- **Walls**: 4 perimeters
- **Supports**: None needed — all pieces print flat
- **Orientation**: Shelves print face-down. Brackets print with the flat (wall) face on the bed.

## Bracket Design

The bracket is a convex arch (like a corbel):
- **Top**: 60mm deep shelf support (full width)
- **Bottom**: 15mm thick wall section (tapers smoothly)
- **Outer surface**: smooth convex curve (bulges into room)
- **Boss**: 12mm raised pad on the wall face around the screw hole
  - The boss protrudes 3mm from the wall face
  - Screw head clamps against the room-side bracket surface
  - Boss presses against the wall (acts as built-in washer)
- **Screw hole**: 4.2mm through-hole at 20% height (near bottom)

## Assembly

1. **Screw brackets to wall** (one per shelf level)
   - Position bracket on one wall, ~50mm from corner
   - Screw through bracket + boss into wall with #8 wood screw
   - Use wall anchor if not hitting a stud
2. **Set shelves on brackets**
   - Shelf straight edges rest against both walls
   - Bracket supports the shelf from below on one wall
   - Corner provides the second support point
3. **Route lamp cord** through cable crescent at upper shelf corner

## Hardware
- 2x #8 wood screws (4mm, 30mm+ long to go through boss + into wall)
- 2x wall anchors (if needed)

## Adjusting
Edit `params.json` and re-run `design.py`:
- `shelf_radius_mm`: shelf size (keep ≤ 180 for single-piece)
- `bracket_depth_mm` / `bracket_height_mm`: bracket leg lengths
- `bracket_min_thickness_mm`: thickness at bottom of bracket (wall section)
- `boss_diameter_mm` / `boss_protrusion_mm`: screw boss size

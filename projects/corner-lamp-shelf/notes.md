# Corner Lamp/Plant Shelf — Print & Assembly Notes

## What This Is

Two-level corner shelf system for a 90-degree wall corner:
- **Upper shelf**: holds an EDISHINE 13.5" table lamp (~220mm shade, ~560g)
- **Lower shelf**: holds a small plant/pot (up to ~150mm pot diameter)
- Cable crescent at the corner of the upper shelf for the lamp cord

## Print List

| File | Qty | Bed fit | Notes |
|---|---|---|---|
| `upper_corner.stl` | 1 | 140x140mm | Corner tile with cable slot |
| `upper_right.stl` | 1 | 140x140mm | Right wall tile with lip |
| `upper_top.stl` | 1 | 140x140mm | Top wall tile with lip |
| `upper_outer.stl` | 1 | 103x103mm | Outer curve tile with lip |
| `lower_shelf.stl` | 1 | 170x170mm | Single piece, fits on A1 Mini |
| `bracket_x4.stl` | 4 | 60x60mm | 2 per shelf level, 1 per wall |

**Total: 9 prints**

## Print Settings

- **Printer**: Bambu A1 Mini (180x180mm bed)
- **Material**: PLA or PETG (PETG preferred for rigidity under load)
- **Layer height**: 0.2mm
- **Infill**: 40-50% (structural — these hold weight)
- **Walls/perimeters**: 4 minimum
- **Top/bottom layers**: 5 minimum
- **Supports**: None needed (all pieces print flat)
- **Brim**: Recommended for `upper_outer.stl` (small contact area)

## Assembly

### Step 1: Glue upper shelf tiles
1. Lay all 4 upper tiles face-down on a flat surface (glass/mirror is ideal)
2. Dry-fit to check alignment
3. Apply CA glue (superglue) or 2-part epoxy to the mating edges
4. Press together on the flat surface — gravity keeps them coplanar
5. Tape with painter's tape while curing
6. Wait 10-15 min (CA) or 1 hour (epoxy)

### Step 2: Mount brackets
1. Hold each bracket against the wall at desired height, vertical face flat against wall
2. Mark screw holes through the bracket
3. Pre-drill with 3mm bit if hitting studs, or install wall anchors
4. Screw brackets in with #8 wood screws (~30mm long)
5. **Upper level**: 2 brackets (1 per wall), positioned ~50mm from the corner
6. **Lower level**: 2 brackets (1 per wall), positioned ~50mm from the corner
7. Vertical spacing between levels: ~300-350mm (enough for the lamp height)

### Step 3: Place shelves
1. Set glued upper shelf on the upper brackets
2. Set lower shelf on the lower brackets
3. Route lamp cord through the cable crescent at the corner and down the wall

## Hardware Needed

- 8x #8 wood screws (4mm diameter, 25-30mm long)
- 8x wall anchors (if not hitting studs — toggle bolts recommended for drywall)
- CA glue or 2-part epoxy for tile joints

## Design Parameters

All dimensions in `params.json`. Key ones to adjust:
- `upper_radius_mm`: increase for a bigger lamp shelf (will generate more/larger tiles)
- `lower_radius_mm`: increase if your pot is larger than 150mm
- `cable_slot_radius_mm`: 12mm fits standard lamp cords; increase for thicker cables
- `bracket_depth_mm`: increase if shelf droops at outer edge under load

## Known Issues / Future Improvements

- v1 has no alignment pins between tiles — rely on flat surface during gluing
- If the outer edge droops under lamp weight, increase infill to 60% or print with PETG
- The lip is on the curved edge only; walls provide the backstop on the straight edges
- Cable crescent is a full circle cutout at origin — could refine to true half-circle facing inward

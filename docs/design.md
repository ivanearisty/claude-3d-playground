# Project Structure Specification

## Directory layout

```
claude-3d-playground/
├── CLAUDE.md                    # Philosophy, conventions, workflow
├── src/claude_3d_playground/    # Shared toolkit (mesh validation, export, OpenSCAD wrapper)
├── projects/                    # Each printable thing is a self-contained project
│   └── <project-name>/
│       ├── design.py            # Parametric source — single source of truth
│       ├── params.json          # All dimensions, tolerances, and options
│       ├── stl/                 # Generated STLs — one file per printable part
│       └── notes.md             # Print settings, assembly instructions, gotchas
├── examples/                    # Standalone demo scripts (not full projects)
├── tests/                       # Unit and integration tests for the toolkit
└── docs/                        # This file and any other documentation
```

## Project directory spec

### `params.json`

A flat or shallow-nested JSON file containing every tunable dimension. This is the only file a user should need to edit to customize a design for their use case.

```json
{
  "wall_thickness": 2.0,
  "tolerance": 0.4,
  "corner_angle": 90,
  "shelf_width": 150,
  "shelf_depth": 120,
  "mount_hole_diameter": 5.0
}
```

Rules:
- All values in millimeters (or degrees for angles)
- Use descriptive keys — `shelf_width` not `w`
- Include a `tolerance` field for any project with interlocking or friction-fit parts
- No computed values — those belong in `design.py`

### `design.py`

The parametric model script. It reads `params.json`, builds the geometry using CadQuery or OpenSCAD, and exports STLs to the `stl/` directory.

Requirements:
- Must be runnable standalone: `uv run python projects/<name>/design.py`
- Reads params from `params.json` in the same directory
- Exports one STL per printable part to `stl/`
- Each part should be oriented for printing (flat side down, minimal supports)
- Prints a summary of what was exported when run

### `stl/`

Generated output directory. Each file is one printable part.

Naming convention:
- Descriptive names: `bracket_left.stl`, `shelf_plate.stl`, `lamp_mount.stl`
- If multiples of the same part: `leg_x4.stl` (the x4 tells you to print 4 copies)
- No `part1.stl`, `output.stl`, etc.

### `notes.md`

Human-readable document covering:
- **Print settings** — layer height, infill %, material, nozzle size
- **Supports** — which parts need them, suggested support type
- **Assembly order** — step-by-step if multi-part
- **Hardware** — any non-printed parts needed (screws, magnets, LEDs, etc.)
- **Known issues** — things that didn't work, tolerances that needed adjustment

## When to use CadQuery vs OpenSCAD

| Use CadQuery when... | Use OpenSCAD when... |
|---|---|
| Complex fillets, chamfers, lofts | Simple boolean operations (union, difference) |
| Assemblies with multiple interacting parts | Quick one-off shapes |
| You need programmatic control (loops, conditionals) | The shape is naturally described as CSG |
| Organic or curved geometry | You want a `.scad` file to share with OpenSCAD users |

Both are valid. Pick whichever makes the design clearer.

## Validation checklist

Before marking a project as done, every STL should pass:
- [ ] Watertight mesh (no holes)
- [ ] Manifold geometry (no self-intersections)
- [ ] Correct bounding box dimensions (matches params)
- [ ] Oriented for printing (flat on build plate)
- [ ] Wall thickness >= 2mm everywhere
- [ ] Overhangs <= 45° or supports noted

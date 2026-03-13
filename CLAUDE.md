# Claude 3D Playground

## Philosophy

This repo is a **workshop, not a library**. The goal is to make 3D printing with Claude Code feel like pair-designing with someone who can actually compile and validate the models. Every project should be:

- **Parametric first** — dimensions live in `params.json`, not buried in code. Changing a measurement should never require understanding the script.
- **One part per STL** — each printable piece gets its own file. No multi-body STLs that need splitting in the slicer.
- **Validate before handing off** — every generated STL gets checked for watertightness, manifold edges, and sane dimensions before the user touches it. Catch print failures at design time.
- **Print-aware** — wall thickness, overhang angles, bridging limits, and tolerance gaps are not afterthoughts. Design for FDM from the start.
- **Self-documenting** — each project has notes on print settings, assembly, and any gotchas so you can reprint in 6 months without reverse-engineering your own work.

## Project structure

See [docs/design.md](docs/design.md) for the full project structure specification.

Quick reference:
```
projects/<project-name>/
  design.py       # parametric source (CadQuery or OpenSCAD)
  params.json     # all dimensions and tolerances
  stl/            # one STL per printable part
  notes.md        # print settings, assembly, gotchas
```

## Conventions

- Use CadQuery for complex/organic geometry, OpenSCAD for simple parametric shapes
- Default tolerance for interlocking parts: 0.4mm (tune per printer)
- Default wall thickness: 2mm minimum (3 perimeters at 0.4mm nozzle)
- All dimensions in millimeters
- STL filenames should describe the part, not be generic (e.g., `bracket_left.stl` not `part1.stl`)

## Available tools

- `src/claude_3d_playground/openscad.py` — compile `.scad` → `.stl`
- `src/claude_3d_playground/mesh.py` — validate and repair STL meshes
- `src/claude_3d_playground/cadquery_utils.py` — export CadQuery workplanes to STL
- System: `openscad` (brew), `admesh` (brew) available on PATH

## Workflow

1. Create a project directory under `projects/`
2. Define parameters in `params.json`
3. Write parametric design in `design.py`
4. Generate STLs, validate meshes, iterate
5. Document print settings in `notes.md`
6. Commit when the design is print-ready

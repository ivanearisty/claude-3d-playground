# Claude 3D Playground

Design, validate, and slice 3D models with Claude Code.

This repo is a toolkit for 3D printing workflows driven by Claude Code. Instead of manually writing OpenSCAD or CAD scripts, describe what you want and Claude will generate the geometry, compile it, validate the mesh, and optionally slice it for your printer.

## System Requirements

```bash
brew install openscad admesh
# Optional: brew install --cask prusaslicer
```

## Setup

```bash
uv sync --all-extras
make setup
```

## What's Inside

| Module | Purpose |
|---|---|
| `openscad.py` | Compile `.scad` files to `.stl` via OpenSCAD CLI |
| `mesh.py` | Load, validate, and repair STL meshes with trimesh |
| `cadquery_utils.py` | Export CadQuery parametric models to STL |

## Usage with Claude Code

Just open this directory in Claude Code and ask for what you need:

- *"Make me a phone stand for my desk, 70mm wide"*
- *"Create a parametric enclosure for a Raspberry Pi 4"*
- *"Validate the STL in models/stl/part.stl and fix any issues"*
- *"Slice models/stl/box.stl for my Prusa MK4"*

Claude will use the utilities in `src/` to generate, compile, and validate everything.

## Running Tests

```bash
make test
```

## Project Structure

```
src/claude_3d_playground/   # Core library
examples/                   # Example scripts and .scad files
models/
  stl/                      # Generated STL files
  scad/                     # OpenSCAD source files
  gcode/                    # Sliced gcode (gitignored)
tests/
```

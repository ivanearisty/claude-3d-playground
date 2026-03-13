"""Example: Generate a simple box with a snap-fit lid using CadQuery."""

from pathlib import Path

import cadquery as cq

from claude_3d_playground import export_cadquery

MODELS_DIR = Path(__file__).parent.parent / "models" / "stl"

# --- Box ---
box_width, box_depth, box_height = 60.0, 40.0, 30.0
wall = 2.0

box = cq.Workplane("XY").box(box_width, box_depth, box_height).faces(">Z").shell(-wall)

# --- Lid ---
lid_height = 5.0
lip = 1.0  # inner lip for snap fit

lid = (
    cq.Workplane("XY")
    .box(box_width, box_depth, lid_height)
    .faces("<Z")
    .workplane()
    .rect(box_width - 2 * wall - 0.4, box_depth - 2 * wall - 0.4)
    .extrude(lip)
)

if __name__ == "__main__":
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    export_cadquery(box, MODELS_DIR / "box.stl")
    export_cadquery(lid, MODELS_DIR / "lid.stl")
    print(f"Exported box and lid to {MODELS_DIR}")

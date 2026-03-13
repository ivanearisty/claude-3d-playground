"""Corner Lamp/Plant Shelf — Single-piece shelves with arch brackets for Bambu A1 Mini.

OuXean mini lamp: 109x109x79mm, 350g.
Both shelves fit as single pieces on the 180mm bed.
Arch brackets with gradual curve and screw holes at the bottom.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).parent
STL = HERE / "stl"
P = json.loads((HERE / "params.json").read_text())


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

def quarter_disk(radius: float, height: float) -> cq.Workplane:
    """Quarter-circle disk in first quadrant (+x, +y), z from 0 to height."""
    full = cq.Workplane("XY").circle(radius).extrude(height)
    clip = (
        cq.Workplane("XY")
        .box(radius + 0.1, radius + 0.1, height + 0.1)
        .translate(((radius + 0.1) / 2, (radius + 0.1) / 2, height / 2))
    )
    return full.intersect(clip)


# ---------------------------------------------------------------------------
# Shelf
# ---------------------------------------------------------------------------

def make_shelf(radius: float, thick: float, lip_h: float, lip_w: float) -> cq.Workplane:
    """Quarter-circle shelf with raised lip on the curved edge."""
    base = quarter_disk(radius, thick)
    if lip_h > 0 and lip_w > 0:
        lip_ring = quarter_disk(radius, thick + lip_h).cut(
            cq.Workplane("XY").circle(radius - lip_w).extrude(thick + lip_h + 1)
        )
        base = base.union(lip_ring)
    return base


def cut_cable_slot(body: cq.Workplane, r: float) -> cq.Workplane:
    """Cut cable passthrough at the corner (origin)."""
    return body.cut(cq.Workplane("XY").circle(r).extrude(500).translate((0, 0, -250)))


# ---------------------------------------------------------------------------
# Arch bracket
# ---------------------------------------------------------------------------

def make_arch_bracket(
    depth: float,
    height: float,
    thick: float,
    width: float,
    screw_d: float,
) -> cq.Workplane:
    """Arch-shaped wall bracket with smooth curve and screw holes at the bottom.

    Profile is an L-shape where the inner corner is a gradual arch instead of a
    sharp angle. Vertical face (x=0) mounts to the wall. Shelf rests on top
    face (y=height). Screw holes are near the bottom of the wall section.

    Orientation when mounted:
        Y = vertical (up the wall)
        X = horizontal (into the room)
        Z = along the wall (bracket width)
    """
    # Midpoint for the arch curve (parametric quarter-ellipse at 45 degrees)
    t = math.pi / 4
    mid_x = thick + (depth - thick) * math.sin(t)
    mid_y = (height - thick) * (1 - math.cos(t))

    # 2D profile: outer L-shape with arched inner contour
    profile = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(thick, 0)                                          # inner wall base
        .threePointArc((mid_x, mid_y), (depth, height - thick))    # arch curve
        .lineTo(depth, height)                                     # shelf outer edge
        .lineTo(0, height)                                         # shelf top to wall
        .close()                                                   # wall outer face
        .extrude(width)
    )

    # Screw holes through the wall face near the bottom
    for y_pos in [12, height * 0.45]:
        hole = (
            cq.Workplane("YZ")
            .center(y_pos, width / 2)
            .circle(screw_d / 2)
            .extrude(depth)
        )
        profile = profile.cut(hole)

    return profile


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def save(wp: cq.Workplane, name: str) -> None:
    """Export workplane to STL and print dimensions."""
    path = STL / name
    cq.exporters.export(wp, str(path))
    bb = wp.val().BoundingBox()
    print(f"  {name:<30s} {bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f} mm")


def main() -> None:
    STL.mkdir(parents=True, exist_ok=True)

    # --- Upper shelf (lamp) ---
    print("Upper shelf (lamp):")
    upper = make_shelf(P["upper_radius_mm"], P["thickness_mm"], P["lip_height_mm"], P["lip_width_mm"])
    upper = cut_cable_slot(upper, P["cable_slot_radius_mm"])
    save(upper, "upper_shelf.stl")

    # --- Lower shelf (plant) ---
    print("\nLower shelf (plant):")
    lower = make_shelf(P["lower_radius_mm"], P["thickness_mm"], P["lip_height_mm"], P["lip_width_mm"])
    save(lower, "lower_shelf.stl")

    # --- Arch brackets ---
    print("\nArch brackets:")
    bracket = make_arch_bracket(
        P["bracket_depth_mm"],
        P["bracket_height_mm"],
        P["bracket_thickness_mm"],
        P["bracket_width_mm"],
        P["screw_diameter_mm"],
    )
    save(bracket, "arch_bracket_x4.stl")

    # --- Summary ---
    print(f"\nAll STLs in {STL.relative_to(HERE)}/")
    print("Print list:")
    print("  1x upper_shelf.stl")
    print("  1x lower_shelf.stl")
    print("  4x arch_bracket_x4.stl (2 per level, 1 per wall)")
    print("  Total: 6 prints")


if __name__ == "__main__":
    main()

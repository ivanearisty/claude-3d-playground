"""Corner Lamp/Plant Shelf — Single-piece shelves with convex arch brackets.

OuXean mini lamp: 109x109x79mm, 350g.
Both shelves single-piece on A1 Mini (180mm bed).
Convex arch brackets with screw boss — 4 prints total.
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
# Shelf
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


def make_shelf(radius: float, thick: float, lip_h: float, lip_w: float) -> cq.Workplane:
    """Quarter-circle shelf with raised lip on curved edge."""
    base = quarter_disk(radius, thick)
    if lip_h > 0 and lip_w > 0:
        lip_ring = quarter_disk(radius, thick + lip_h).cut(
            cq.Workplane("XY").circle(radius - lip_w).extrude(thick + lip_h + 1)
        )
        base = base.union(lip_ring)
    return base


def cut_cable_slot(body: cq.Workplane, r: float) -> cq.Workplane:
    """Cut cable passthrough at the corner origin."""
    return body.cut(cq.Workplane("XY").circle(r).extrude(500).translate((0, 0, -250)))


# ---------------------------------------------------------------------------
# Convex arch bracket
# ---------------------------------------------------------------------------

def make_arch_bracket(
    depth: float,
    height: float,
    min_thick: float,
    width: float,
    screw_d: float,
    boss_d: float,
    boss_h: float,
) -> cq.Workplane:
    """Convex arch bracket with screw boss.

    Thickest at the top (shelf support = depth), tapers to min_thick at the
    bottom (wall mount). The room-facing surface is a smooth convex curve.
    A boss protrudes from the wall face around the screw hole.

    When mounted on wall:
        X = into room (depth direction)
        Y = up the wall (height direction)
        Z = along the wall (bracket width)
    """
    # Compute convex curve midpoint
    # Line from (min_thick, 0) to (depth, height) — push perpendicular into room
    dx = depth - min_thick
    dy = height
    line_len = math.sqrt(dx**2 + dy**2)
    perp_x = dy / line_len   # perpendicular component pointing into room
    perp_y = -dx / line_len  # perpendicular component pointing down
    bulge = line_len * 0.2   # 20% outward bulge
    mid_x = (min_thick + depth) / 2 + bulge * perp_x
    mid_y = height / 2 + bulge * perp_y

    # 2D profile: straight L on inside, convex curve on outside
    bracket = (
        cq.Workplane("XY")
        .moveTo(0, 0)                                       # wall bottom
        .lineTo(min_thick, 0)                                # inner bottom edge
        .threePointArc((mid_x, mid_y), (depth, height))      # convex outer curve
        .lineTo(0, height)                                   # shelf top back to wall
        .close()                                             # down the wall face
        .extrude(width)
    )

    # Boss: raised cylinder on wall face (protrudes toward wall, -X direction)
    screw_y = height * 0.2  # screw at 20% up from bottom
    boss = (
        cq.Workplane("YZ")
        .center(screw_y, width / 2)
        .circle(boss_d / 2)
        .extrude(boss_h)
        .translate((-boss_h, 0, 0))
    )
    bracket = bracket.union(boss)

    # Screw through-hole (from behind boss, all the way through bracket)
    hole = (
        cq.Workplane("YZ")
        .center(screw_y, width / 2)
        .circle(screw_d / 2)
        .extrude(depth + boss_h + 2)
        .translate((-boss_h - 1, 0, 0))
    )
    bracket = bracket.cut(hole)

    return bracket


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def save(wp: cq.Workplane, name: str) -> None:
    """Export to STL and print info."""
    path = STL / name
    cq.exporters.export(wp, str(path))
    bb = wp.val().BoundingBox()
    print(f"  {name:<30s} {bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f} mm")


def main() -> None:
    STL.mkdir(parents=True, exist_ok=True)

    r = P["shelf_radius_mm"]
    t = P["shelf_thickness_mm"]

    print("Upper shelf (lamp):")
    upper = cut_cable_slot(
        make_shelf(r, t, P["lip_height_mm"], P["lip_width_mm"]),
        P["cable_slot_radius_mm"],
    )
    save(upper, "upper_shelf.stl")

    print("\nLower shelf (plant):")
    lower = make_shelf(r, t, P["lip_height_mm"], P["lip_width_mm"])
    save(lower, "lower_shelf.stl")

    print("\nArch bracket:")
    bracket = make_arch_bracket(
        P["bracket_depth_mm"],
        P["bracket_height_mm"],
        P["bracket_min_thickness_mm"],
        P["bracket_width_mm"],
        P["screw_diameter_mm"],
        P["boss_diameter_mm"],
        P["boss_protrusion_mm"],
    )
    save(bracket, "arch_bracket_x2.stl")

    print(f"\nAll STLs in {STL.relative_to(HERE)}/")
    print("Print list:")
    print("  1x upper_shelf.stl (with cable slot)")
    print("  1x lower_shelf.stl")
    print("  2x arch_bracket_x2.stl (1 per shelf level)")
    print("  Total: 4 prints")


if __name__ == "__main__":
    main()

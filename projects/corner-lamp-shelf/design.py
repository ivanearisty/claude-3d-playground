"""Corner Lamp/Plant Shelf — Parametric two-level corner shelf for Bambu A1 Mini (180mm bed).

Upper shelf (lamp): 280mm radius quarter circle, split into 4 tiles.
Lower shelf (plant): 170mm radius quarter circle, single piece.
Cable crescent at the corner of the upper shelf for the lamp cord.
Triangular wall brackets for mounting.
"""

from __future__ import annotations

import json
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
    """Cut semicircle cable passthrough at the corner (origin)."""
    cutter = cq.Workplane("XY").circle(r).extrude(500).translate((0, 0, -250))
    return body.cut(cutter)


# ---------------------------------------------------------------------------
# Tile splitting
# ---------------------------------------------------------------------------

def split_tiles(body: cq.Workplane, radius: float) -> list[tuple[str, cq.Workplane]]:
    """Split shelf into 2x2 grid tiles that each fit on the printer bed."""
    h = radius / 2
    grid = {"corner": (0, 0), "right": (1, 0), "top": (0, 1), "outer": (1, 1)}
    out = []
    for name, (c, r) in grid.items():
        clip = (
            cq.Workplane("XY")
            .box(h + 0.02, h + 0.02, 500)
            .translate((c * h + h / 2, r * h + h / 2, 0))
        )
        piece = body.intersect(clip)
        if piece.val().Volume() > 1:
            out.append((name, piece))
    return out


# ---------------------------------------------------------------------------
# Bracket
# ---------------------------------------------------------------------------

def make_bracket(depth: float, height: float, width: float, screw_d: float) -> cq.Workplane:
    """Triangular wall bracket. Vertical face (x=0) screws to wall, shelf rests on y=0 face."""
    tri = (
        cq.Workplane("XY")
        .polyline([(0, 0), (depth, 0), (0, height)])
        .close()
        .extrude(width)
    )
    # Screw hole through the wall face at 60% height, centered in width
    hole = (
        cq.Workplane("YZ")
        .center(height * 0.6, width / 2)
        .circle(screw_d / 2)
        .extrude(depth)
    )
    return tri.cut(hole)


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
    bed = P["printer_bed_mm"]

    # --- Upper shelf (lamp) ---
    print("Upper shelf (lamp):")
    upper = make_shelf(P["upper_radius_mm"], P["thickness_mm"], P["lip_height_mm"], P["lip_width_mm"])
    upper = cut_cable_slot(upper, P["cable_slot_radius_mm"])

    if P["upper_radius_mm"] / 2 <= bed:
        for name, tile in split_tiles(upper, P["upper_radius_mm"]):
            save(tile, f"upper_{name}.stl")
    else:
        save(upper, "upper_shelf.stl")

    # --- Lower shelf (plant) ---
    print("\nLower shelf (plant):")
    lower = make_shelf(P["lower_radius_mm"], P["thickness_mm"], P["lip_height_mm"], P["lip_width_mm"])

    if P["lower_radius_mm"] <= bed:
        save(lower, "lower_shelf.stl")
    else:
        for name, tile in split_tiles(lower, P["lower_radius_mm"]):
            save(tile, f"lower_{name}.stl")

    # --- Brackets ---
    print("\nBrackets:")
    b = make_bracket(
        P["bracket_depth_mm"], P["bracket_height_mm"],
        P["bracket_width_mm"], P["screw_diameter_mm"],
    )
    save(b, "bracket_x4.stl")

    # --- Summary ---
    print(f"\nAll STLs exported to {STL.relative_to(HERE)}/")
    upper_tiles = split_tiles(upper, P["upper_radius_mm"])
    print("Print list:")
    print(f"  {len(upper_tiles)}x upper shelf tiles (glue together)")
    if P["lower_radius_mm"] <= bed:
        print("  1x lower_shelf.stl")
    print("  4x bracket_x4.stl (2 per shelf level, 1 per wall)")


if __name__ == "__main__":
    main()

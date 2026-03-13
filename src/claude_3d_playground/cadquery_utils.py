"""CadQuery helpers — parametric CAD in Python, exported to STL."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import cadquery as cq


def export_cadquery(
    workplane: cq.Workplane,
    output_path: str | Path,
    *,
    tolerance: float = 0.1,
    angular_tolerance: float = 0.1,
) -> Path:
    """Export a CadQuery Workplane to STL.

    Args:
        workplane: A CadQuery Workplane with geometry.
        output_path: Where to write the .stl file.
        tolerance: Linear tolerance for tessellation (mm).
        angular_tolerance: Angular tolerance for tessellation (degrees).

    Returns:
        Path to the exported .stl file.

    """
    import cadquery as cq  # noqa: PLC0415

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cq.exporters.export(
        workplane,
        str(output_path),
        exportType=cq.exporters.ExportTypes.STL,
        tolerance=tolerance,
        angularTolerance=angular_tolerance,
    )
    return output_path

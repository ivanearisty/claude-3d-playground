"""Mesh loading, validation, and repair utilities using trimesh."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import trimesh

if TYPE_CHECKING:
    import numpy as np


@dataclass
class MeshReport:
    """Summary of mesh health."""

    path: str
    triangle_count: int
    vertex_count: int
    is_watertight: bool
    is_volume: bool
    bounding_box_mm: tuple[float, float, float]
    volume_mm3: float | None
    errors: list[str]

    @property
    def is_valid(self) -> bool:
        """Mesh is printable if watertight and has volume."""
        return self.is_watertight and self.is_volume and len(self.errors) == 0


def load_stl(path: str | Path) -> trimesh.Trimesh:
    """Load an STL file and return a trimesh object."""
    path = Path(path)
    if not path.exists():
        msg = f"STL file not found: {path}"
        raise FileNotFoundError(msg)
    mesh = trimesh.load(str(path), file_type="stl")
    if not isinstance(mesh, trimesh.Trimesh):
        msg = f"Expected a single mesh, got {type(mesh).__name__}"
        raise TypeError(msg)
    return mesh


def validate_mesh(path: str | Path) -> MeshReport:
    """Load an STL and produce a printability report."""
    mesh = load_stl(path)
    extents: np.ndarray = mesh.bounding_box.extents  # type: ignore[union-attr]

    errors: list[str] = []
    if not mesh.is_watertight:
        errors.append("Mesh is not watertight (has holes)")
    if not mesh.is_volume:
        errors.append("Mesh does not enclose a volume")
    if mesh.body_count > 1:  # type: ignore[operator]
        errors.append(f"Mesh has {mesh.body_count} disconnected bodies")

    return MeshReport(
        path=str(path),
        triangle_count=len(mesh.faces),
        vertex_count=len(mesh.vertices),
        is_watertight=bool(mesh.is_watertight),
        is_volume=bool(mesh.is_volume),
        bounding_box_mm=(float(extents[0]), float(extents[1]), float(extents[2])),
        volume_mm3=float(mesh.volume) if mesh.is_volume else None,
        errors=errors,
    )


def repair_mesh(path: str | Path, output_path: str | Path | None = None) -> Path:
    """Attempt basic mesh repair (fill holes, merge vertices) and save."""
    mesh = load_stl(path)
    trimesh.repair.fix_normals(mesh)
    trimesh.repair.fix_winding(mesh)
    trimesh.repair.fill_holes(mesh)

    if output_path is None:
        p = Path(path)
        output_path = p.parent / f"{p.stem}_repaired.stl"
    else:
        output_path = Path(output_path)

    mesh.export(str(output_path), file_type="stl")
    return output_path

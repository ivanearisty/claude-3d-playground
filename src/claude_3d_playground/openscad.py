"""OpenSCAD wrapper — compile .scad files to .stl via CLI."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def find_openscad() -> str:
    """Locate the OpenSCAD binary."""
    path = shutil.which("openscad")
    if path is None:
        msg = "OpenSCAD not found. Install with: brew install openscad"
        raise FileNotFoundError(msg)
    return path


def render_scad(
    scad_path: str | Path,
    output_path: str | Path | None = None,
    *,
    timeout: int = 120,
) -> Path:
    """Render a .scad file to .stl using OpenSCAD CLI.

    Args:
        scad_path: Path to the .scad source file.
        output_path: Where to write the .stl. Defaults to same name with .stl extension.
        timeout: Max seconds to wait for rendering.

    Returns:
        Path to the generated .stl file.

    """
    scad_path = Path(scad_path)
    if not scad_path.exists():
        msg = f"SCAD file not found: {scad_path}"
        raise FileNotFoundError(msg)

    output_path = scad_path.with_suffix(".stl") if output_path is None else Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    openscad = find_openscad()
    result = subprocess.run(  # noqa: S603
        [openscad, "-o", str(output_path), str(scad_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        msg = f"OpenSCAD failed:\n{result.stderr}"
        raise RuntimeError(msg)

    return output_path


def render_scad_string(
    scad_code: str,
    output_path: str | Path,
    *,
    timeout: int = 120,
) -> Path:
    """Render OpenSCAD code from a string (writes a temp .scad file, then compiles).

    Args:
        scad_code: OpenSCAD source code as a string.
        output_path: Where to write the .stl.
        timeout: Max seconds to wait for rendering.

    Returns:
        Path to the generated .stl file.

    """
    output_path = Path(output_path)
    scad_path = output_path.with_suffix(".scad")
    scad_path.write_text(scad_code)
    return render_scad(scad_path, output_path, timeout=timeout)

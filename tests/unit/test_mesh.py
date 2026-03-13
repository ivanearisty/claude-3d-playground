"""Unit tests for mesh utilities."""

from __future__ import annotations

import pytest

from claude_3d_playground.mesh import validate_mesh
from claude_3d_playground.openscad import render_scad_string


@pytest.fixture
def cube_stl(tmp_path: pytest.TempPathFactory) -> str:  # type: ignore[type-arg]
    """Generate a simple cube STL for testing."""
    output = tmp_path / "cube.stl"  # type: ignore[operator]
    render_scad_string("cube([10, 10, 10]);", output)
    return str(output)


class TestValidateMesh:
    """Tests for mesh validation."""

    def test_cube_is_valid(self, cube_stl: str) -> None:
        report = validate_mesh(cube_stl)
        assert report.is_valid
        assert report.is_watertight
        assert report.triangle_count > 0

    def test_cube_dimensions(self, cube_stl: str) -> None:
        report = validate_mesh(cube_stl)
        x, y, z = report.bounding_box_mm
        assert abs(x - 10.0) < 0.01
        assert abs(y - 10.0) < 0.01
        assert abs(z - 10.0) < 0.01

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            validate_mesh("/nonexistent/file.stl")

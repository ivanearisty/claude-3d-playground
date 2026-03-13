"""Unit tests for the OpenSCAD wrapper."""

from __future__ import annotations

import pytest

from claude_3d_playground.openscad import find_openscad, render_scad_string


class TestFindOpenscad:
    """Tests for locating the OpenSCAD binary."""

    def test_finds_openscad(self) -> None:
        path = find_openscad()
        assert "openscad" in path.lower()


class TestRenderScadString:
    """Tests for rendering OpenSCAD code from a string."""

    def test_renders_cube(self, tmp_path: pytest.TempPathFactory) -> None:  # type: ignore[type-arg]
        output = tmp_path / "cube.stl"  # type: ignore[operator]
        result = render_scad_string("cube([10, 10, 10]);", output)
        assert result.exists()
        assert result.stat().st_size > 0

    def test_invalid_scad_raises(self, tmp_path: pytest.TempPathFactory) -> None:  # type: ignore[type-arg]
        output = tmp_path / "bad.stl"  # type: ignore[operator]
        with pytest.raises(RuntimeError, match="OpenSCAD failed"):
            render_scad_string("this is not valid scad }{}{", output)

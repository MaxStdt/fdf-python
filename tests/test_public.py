"""Публичные тесты стартового набора.

Фиксируют имена модулей, классов, функций и сигнатуры пакета fdf.
Если этот файл падает — значит, кто-то переименовал публичную сущность,
и стартовый набор перестанет работать.
"""
from __future__ import annotations

import importlib
import inspect

import pytest

# ---------------------------------------------------------------------------
# 1. Пакет fdf и его модули
# ---------------------------------------------------------------------------

def test_package_fdf_importable() -> None:
    """Пакет fdf существует и импортируется."""
    import fdf  # noqa: F401


@pytest.mark.parametrize("module_name", [
    "fdf.errors",
    "fdf.parser",
    "fdf.model",
    "fdf.projection",
    "fdf.app",
])
def test_public_modules_exist(module_name: str) -> None:
    """Все публичные модули пакета существуют и импортируются."""
    module = importlib.import_module(module_name)
    assert module is not None

# ---------------------------------------------------------------------------
# 2. Классы и функции в модулях
# ---------------------------------------------------------------------------

def test_errors_exports() -> None:
    """errors.py экспортирует FdfError и MapFormatError."""
    from fdf import errors
    assert hasattr(errors, "FdfError")
    assert hasattr(errors, "MapFormatError")
    assert issubclass(errors.MapFormatError, errors.FdfError)
    assert issubclass(errors.FdfError, Exception)


def test_parser_exports() -> None:
    """parser.py экспортирует parse_map."""
    from fdf import parser
    assert hasattr(parser, "parse_map")
    assert callable(parser.parse_map)


def test_model_exports() -> None:
    """model.py экспортирует Point и Map."""
    from fdf import model
    assert hasattr(model, "Point")
    assert hasattr(model, "Map")
    assert inspect.isclass(model.Point)
    assert inspect.isclass(model.Map)


def test_projection_exports() -> None:
    """projection.py экспортирует Camera и project."""
    from fdf import projection
    assert hasattr(projection, "Camera")
    assert hasattr(projection, "project")
    assert inspect.isclass(projection.Camera)
    assert callable(projection.project)


def test_app_exports() -> None:
    """app.py экспортирует App (GUI-класс)."""
    from fdf import app
    assert hasattr(app, "App")
    assert inspect.isclass(app.App)


# ---------------------------------------------------------------------------
# 3. Сигнатуры публичных функций и методов
# ---------------------------------------------------------------------------

def test_parse_map_signature() -> None:
    """parse_map(path) -> Map."""
    from fdf.parser import parse_map
    sig = inspect.signature(parse_map)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].name == "path"


def test_point_fields() -> None:
    """Point имеет поля x, y, z, color."""
    import dataclasses

    from fdf.model import Point
    assert dataclasses.is_dataclass(Point)
    field_names = {f.name for f in dataclasses.fields(Point)}
    assert {"x", "y", "z", "color"} <= field_names


def test_map_methods() -> None:
    """Map имеет point, neighbors, __len__, __iter__."""
    from fdf.model import Map
    assert hasattr(Map, "point")
    assert hasattr(Map, "neighbors")
    assert hasattr(Map, "__len__")
    assert hasattr(Map, "__iter__")
    sig_point = inspect.signature(Map.point)
    assert list(sig_point.parameters) == ["self", "y", "x"]
    sig_nb = inspect.signature(Map.neighbors)
    assert list(sig_nb.parameters) == ["self", "y", "x"]


def test_camera_methods() -> None:
    """Camera имеет fit и apply."""
    from fdf.projection import Camera
    assert hasattr(Camera, "fit")
    assert hasattr(Camera, "apply")
    sig_fit = inspect.signature(Camera.fit)
    params = list(sig_fit.parameters)
    # self, map_, width, height, z_scale
    assert params[0] == "self"
    assert "map_" in params
    assert "width" in params
    assert "height" in params
    assert "z_scale" in params


def test_project_signature() -> None:
    """project(point, scale, offset_x, offset_y, z_scale=1.0)."""
    from fdf.projection import project
    sig = inspect.signature(project)
    params = list(sig.parameters)
    assert params[0] == "point"
    assert "scale" in params
    assert "offset_x" in params
    assert "offset_y" in params
    assert "z_scale" in params


def test_app_constructor_signature() -> None:
    """App(map_, title=...) — можно создать без открытия окна в тесте."""
    from fdf.app import App
    sig = inspect.signature(App.__init__)
    params = list(sig.parameters)
    assert params[0] == "self"
    assert "map_" in params
    assert "title" in params


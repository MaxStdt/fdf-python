from fdf.model import Point
from fdf.parser import parse_map
from fdf.projection import Camera, project


def test_origin_projects_to_origin() -> None:
    x, y = project(Point(0, 0, 0), 1.0, 0.0, 0.0)
    assert abs(x) < 1e-9 and abs(y) < 1e-9


def test_height_moves_up() -> None:
    _, y0 = project(Point(0, 0, 0), 1.0, 0.0, 0.0)
    _, y1 = project(Point(0, 0, 1), 1.0, 0.0, 0.0)
    assert y1 < y0


def test_fit_keeps_points_inside() -> None:
    m = parse_map("maps/elem.fdf")
    cam = Camera()
    cam.fit(m, 800, 600)
    for p in m:
        x, y = cam.apply(p)
        assert -1 <= x <= 801
        assert -1 <= y <= 601
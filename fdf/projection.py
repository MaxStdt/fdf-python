from __future__ import annotations

import math
from dataclasses import dataclass

from .model import Map, Point

COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))


@dataclass
class ProjectedPoint:
    x: float
    y: float
    color: str | None


def project(point: Point, scale: float, offset_x: float,
            offset_y: float, z_scale: float = 1.0) -> tuple[float, float]:
    xp = (point.x - point.y) * COS30
    yp = (point.x + point.y) * SIN30 - point.z * z_scale
    return xp * scale + offset_x, yp * scale + offset_y


class Camera:
    """Хранит масштаб и смещение, умеет подгонять карту под окно."""

    def __init__(self) -> None:
        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.z_scale = 1.0

    def fit(self, map_: Map, width: int, height: int,
            z_scale: float = 1.0) -> None:
        self.z_scale = z_scale
        xs: list[float] = []
        ys: list[float] = []
        for p in map_:
            x, y = project(p, 1.0, 0.0, 0.0, z_scale)
            xs.append(x)
            ys.append(y)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x
        h = max_y - min_y
        w = w if w > 1e-9 else 1.0
        h = h if h > 1e-9 else 1.0
        self.scale = min(width / w, height / h) * 0.9
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2
        self.offset_x = width / 2 - cx * self.scale
        self.offset_y = height / 2 - cy * self.scale

    def apply(self, point: Point) -> tuple[float, float]:
        return project(point, self.scale, self.offset_x,
                       self.offset_y, self.z_scale)
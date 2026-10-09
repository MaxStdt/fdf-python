from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int
    color: str | None = None

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y}, z={self.z})"


class Map:
    """Карта высот: матрица точек rows x cols."""

    def __init__(self, points: list[list[Point]]) -> None:
        if not points or not points[0]:
            raise ValueError("Карта не может быть пустой")
        width = len(points[0])
        for row in points:
            if len(row) != width:
                raise ValueError("Строки карты должны быть одинаковой длины")
        self._points = points
        self.height = len(points)
        self.width = width

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        for row in self._points:
            yield from row

    def point(self, y: int, x: int) -> Point:
        return self._points[y][x]

    def neighbors(self, y: int, x: int) -> list[Point]:
        """Соседи справа и снизу (рёбра строятся один раз)."""
        result: list[Point] = []
        if x + 1 < self.width:
            result.append(self._points[y][x + 1])
        if y + 1 < self.height:
            result.append(self._points[y + 1][x])
        return result
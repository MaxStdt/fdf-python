from __future__ import annotations

import re

from .errors import MapFormatError
from .model import Map, Point

_COLOR_RE = re.compile(r"^0[xX][0-9a-fA-F]{1,6}$")
_VALUE_RE = re.compile(r"^-?\d+$")


def _parse_color(token: str, line: int, column: int) -> str:
    if not _COLOR_RE.match(token):
        raise MapFormatError(line, column, f"'{token}' — некорректный цвет")
    hex_part = token[2:]
    value = int(hex_part, 16)
    if len(hex_part) > 6:
        raise MapFormatError(line, column, f"'{token}' — цвет длиннее 6 цифр")
    return f"#{value:06X}"


def _parse_line(raw: str, line_no: int) -> list[Point]:
    tokens = raw.split()
    points: list[Point] = []
    for col_no, token in enumerate(tokens, start=1):
        if "," in token:
            value_part, color_part = token.split(",", 1)
            color = _parse_color(color_part, line_no, col_no)
        else:
            value_part, color = token, None
        if not _VALUE_RE.match(value_part):
            raise MapFormatError(
                line_no, col_no, f"'{value_part}' — не целое число"
            )
        points.append(Point(x=col_no - 1, y=line_no - 1,
                            z=int(value_part), color=color))
    return points


def parse_map(path: str) -> Map:
    """Читает файл .fdf и возвращает Map.

    OSError не перехватывается — обрабатывается в main.py.
    """
    with open(path, encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()

    if not raw_lines:
        raise MapFormatError(1, 1, "файл пуст")

    rows: list[list[Point]] = []
    for idx, raw in enumerate(raw_lines, start=1):
        if not raw.strip():
            raise MapFormatError(idx, 1, "пустая строка внутри карты")
        rows.append(_parse_line(raw, idx))

    first_len = len(rows[0])
    for idx, row in enumerate(rows, start=1):
        if len(row) != first_len:
            raise MapFormatError(
                idx, len(row) + 1,
                f"разная длина строк: ожидалось {first_len}, получено {len(row)}"
            )
    return Map(rows)
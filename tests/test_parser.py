import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map


def test_elem_map_size_and_center() -> None:
    m = parse_map("maps/elem.fdf")
    assert m.width == 5
    assert m.height == 5
    assert m.point(2, 2).z == 5
    assert m.point(0, 0).x == 0 and m.point(0, 0).y == 0


@pytest.mark.parametrize("bad_file", [
    "maps/bad/empty.fdf",
    "maps/bad/ragged.fdf",
    "maps/bad/non_integer.fdf",
    "maps/bad/bad_color.fdf",
    "maps/bad/bad_color_short.fdf",
])
def test_bad_maps_raise(bad_file: str) -> None:
    with pytest.raises(MapFormatError):
        parse_map(bad_file)


@pytest.mark.parametrize("token,expected_z,expected_color", [
    ("7", 7, None),
    ("-3", -3, None),
    ("2,0xFF8800", 2, "#FF8800"),
    ("1,0xff", 1, "#0000FF"),
])
def test_parse_values(tmp_path, token, expected_z, expected_color) -> None:
    p = tmp_path / "map.fdf"
    p.write_text(f"{token} {token}\n{token} {token}\n", encoding="utf-8")
    m = parse_map(str(p))
    assert m.point(0, 0).z == expected_z
    assert m.point(0, 0).color == expected_color


def test_error_contains_line_and_column() -> None:
    with pytest.raises(MapFormatError) as exc:
        parse_map("maps/bad/non_integer.fdf")
    assert exc.value.line == 2
    assert exc.value.column == 2
    assert "не целое число" in str(exc.value)
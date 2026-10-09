from fdf.parser import parse_map


def test_len_and_iteration() -> None:
    m = parse_map("maps/elem.fdf")
    assert len(m) == 25
    count = 0
    for _p in m:
        count += 1
    assert count == 25


def test_neighbors_corner() -> None:
    m = parse_map("maps/elem.fdf")
    assert len(m.neighbors(0, 0)) == 2
    assert len(m.neighbors(4, 4)) == 0
    assert len(m.neighbors(0, 4)) == 1
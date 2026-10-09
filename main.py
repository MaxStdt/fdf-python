from __future__ import annotations

import sys

from fdf.errors import MapFormatError
from fdf.parser import parse_map

USAGE = "Использование: python main.py <файл.fdf>"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        parse_map(argv[1])
    except OSError as exc:
        print(f"Ошибка ввода-вывода: {exc}", file=sys.stderr)
        return 1
    except MapFormatError as exc:
        print(f"Ошибка формата карты: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
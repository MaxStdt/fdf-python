class FdfError(Exception):
    """Базовое исключение проекта."""


class MapFormatError(FdfError):
    """Ошибка формата файла карты."""

    def __init__(self, line: int, column: int, message: str) -> None:
        self.line = line
        self.column = column
        self.message = message
        super().__init__(f"строка {line}, колонка {column}: {message}")
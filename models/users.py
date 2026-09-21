from models.meters import Meter
from models.readings import Reading


class User:
    """Пользователь системы."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.meters: list[Meter] = []
        self.readings: list[Reading] = []

    def __str__(self) -> str:
        return f"Пользователь: {self.name}"
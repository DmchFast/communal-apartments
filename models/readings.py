from datetime import datetime
from typing import Any


class Reading:
    """Показание счётчика."""

    def __init__(
        self,
        meter_id: int,
        value: float,
        date: str | None = None,
        time: str | None = None,
    ) -> None:
        self.meter_id = meter_id
        self.value = value
        if date is None or time is None:
            now = datetime.now()
            self.date = now.date().isoformat()
            self.time = now.time().strftime("%H:%M:%S")
        else:
            self.date = date
            self.time = time

    def __str__(self) -> str:
        return f"{self.date} {self.time} - {self.value}"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Reading":
        """Создать объект из данных JSON."""
        return cls(
            meter_id=int(data["meter_id"]),
            value=data["value"],
            date=data.get("date"),
            time=data.get("time"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать объект в данные для JSON."""
        return {
            "meter_id": self.meter_id,
            "value": self.value,
            "date": self.date,
            "time": self.time,
        }


def add_reading(readings: list[Reading], meter_id: int, value: float) -> Reading:
    """Добавить показание."""
    reading = Reading(meter_id, value)
    readings.append(reading)
    return reading


def delete_reading(readings: list[Reading], meter_id: int, index: int) -> bool:
    """Удалить показание по индексу в истории."""
    history = get_history(readings, meter_id)
    if index < 0 or index >= len(history):
        return False
    target = history[index]
    readings.remove(target)
    return True


def get_history(readings: list[Reading], meter_id: int) -> list[Reading]:
    """Получить историю показаний по счётчику."""
    return [r for r in readings if r.meter_id == meter_id]


def calculate_consumption(
    readings: list[Reading], meter_id: int
) -> float | None:
    """Вычислить расход между последними показаниями."""
    history = get_history(readings, meter_id)
    if len(history) < 2:
        return None
    return history[-1].value - history[-2].value

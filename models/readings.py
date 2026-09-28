from __future__ import annotations

from datetime import datetime
from typing import Any

from models.meters import Meter


class Reading:
    """Показание счётчика."""

    def __init__(
        self,
        meter: Meter | int,
        value: float,
        date: str | None = None,
        time: str | None = None,
    ) -> None:
        if isinstance(meter, int):
            meter = Meter(meter, f"Счётчик {meter}", "")
        self.meter = meter
        self.meter_id = meter.id
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
            meter=int(data["meter_id"]),
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


def add_reading(
    readings: list[Reading],
    meter: Meter | int,
    value: float,
    attached_meter: Meter | None = None,
) -> Reading:
    """Добавить показание с обязательной связью со счётчиком."""
    if attached_meter is not None:
        meter = attached_meter
    reading = Reading(meter, value)
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
    return [r for r in readings if r.meter.id == meter_id]


def calculate_consumption(
    readings: list[Reading], meter_id: int
) -> float | None:
    """Вернуть расход через главную сущность Payment."""
    from models.payments import create_payment

    payment = create_payment(readings, meter_id)
    return None if payment is None else payment.consumption

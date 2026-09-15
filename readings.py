from datetime import datetime
from typing import Any


def add_reading(
    readings: list[dict[str, Any]], meter_id: int, value: float
) -> dict[str, Any]:
    '''Показания с текущей датой и временем.'''
    now = datetime.now()
    record = {
        "meter_id": meter_id,
        "value": value,
        "date": now.date().isoformat(),
        "time": now.time().strftime("%H:%M:%S"),
    }
    readings.append(record)
    return record


def get_history(
    readings: list[dict[str, Any]], meter_id: int
) -> list[dict[str, Any]]:
    return [r for r in readings if r["meter_id"] == meter_id]


def calculate_consumption(
    readings: list[dict[str, Any]], meter_id: int
) -> float | None:
    '''Вычисление расхода между последними показаниями.'''
    history = get_history(readings, meter_id)
    if len(history) < 2:
        return None
    return history[-1]["value"] - history[-2]["value"]

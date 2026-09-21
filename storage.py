import json
from pathlib import Path
from typing import Any

from models.meters import Meter
from models.readings import Reading

METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"


def load_json(filename: str) -> Any:
    """Загрузка данных из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json(filename: str, data: Any) -> None:
    """Сохранение данных в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_user_meters(username: str) -> list[Meter]:
    """Загрузить счётчики пользователя как объекты Meter."""
    all_data = load_json(METERS_FILE) or {}
    user_data = all_data.get(username, {})
    return [
        Meter.from_data(int(meter_id), data)
        for meter_id, data in user_data.items()
    ]


def save_user_meters(username: str, meters: list[Meter]) -> None:
    """Сохранить счётчики пользователя в JSON."""
    all_data = load_json(METERS_FILE) or {}
    all_data[username] = {str(m.id): m.to_dict() for m in meters}
    save_json(METERS_FILE, all_data)


def load_user_readings(username: str) -> list[Reading]:
    """Загрузить показания пользователя как объекты Reading."""
    all_data = load_json(READINGS_FILE) or {}
    user_readings = all_data.get(username, [])
    return [Reading.from_data(item) for item in user_readings]


def save_user_readings(username: str, readings: list[Reading]) -> None:
    """Сохранить показания пользователя в JSON."""
    all_data = load_json(READINGS_FILE) or {}
    all_data[username] = [r.to_dict() for r in readings]
    save_json(READINGS_FILE, all_data)
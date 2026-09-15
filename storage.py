import json
from pathlib import Path
from typing import Any


METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"


def load_json(filename: str) -> Any:
    # Загрузка данных из JSON-файла.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json(filename: str, data: Any) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Счётчики пользователя.
def load_user_meters(username: str) -> dict[int, dict[str, Any]]:
    all_data = load_json(METERS_FILE) or {}
    user_data = all_data.get(username, {})
    return {int(meter_id): data for meter_id, data in user_data.items()}


def save_user_meters(
    username: str, meters: dict[int, dict[str, Any]]
) -> None:
    all_data = load_json(METERS_FILE) or {}
    all_data[username] = {str(k): v for k, v in meters.items()}
    save_json(METERS_FILE, all_data)


# Показания пользователя.
def load_user_readings(username: str) -> list[dict[str, Any]]:
    all_data = load_json(READINGS_FILE) or {}
    user_readings = all_data.get(username, [])
    for reading in user_readings:
        reading["meter_id"] = int(reading["meter_id"])
    return user_readings


def save_user_readings(
    username: str, readings: list[dict[str, Any]]
) -> None:
    all_data = load_json(READINGS_FILE) or {}
    all_data[username] = readings
    save_json(READINGS_FILE, all_data)

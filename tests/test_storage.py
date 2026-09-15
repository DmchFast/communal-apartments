import json
from pathlib import Path

from storage import (
    load_user_meters,
    save_user_meters,
    load_user_readings,
    save_user_readings,
)


def test_save_and_load_user_meters(tmp_path: Path, monkeypatch) -> None:
    """Проверяет сохранение и загрузку счётчиков пользователя."""
    # Перенаправляем файл данных во временную папку
    monkeypatch.setattr("storage.METERS_FILE", str(tmp_path / "meters.json"))

    meters: dict[int, dict] = {
        1: {"name": "Вода", "unit": "м^3", "tariff": None},
        2: {"name": "Газ", "unit": "м^3", "tariff": 7.5},
    }
    save_user_meters("test_user", meters)
    loaded = load_user_meters("test_user")

    assert loaded == meters


def test_load_user_meters_returns_empty_for_unknown_user(
    tmp_path: Path, monkeypatch
) -> None:
    """Проверяет, что для неизвестного пользователя возвращается пустой словарь."""
    monkeypatch.setattr("storage.METERS_FILE", str(tmp_path / "meters.json"))

    assert load_user_meters("unknown") == {}


def test_save_and_load_user_readings(
    tmp_path: Path, monkeypatch
) -> None:
    """Проверяет сохранение и загрузку показаний пользователя."""
    monkeypatch.setattr("storage.READINGS_FILE", str(tmp_path / "readings.json"))

    readings = [
        {"meter_id": 1, "value": 100.0, "date": "2026-09-15", "time": "10:00:00"},
        {"meter_id": 1, "value": 150.0, "date": "2026-09-16", "time": "11:00:00"},
    ]
    save_user_readings("test_user", readings)
    loaded = load_user_readings("test_user")

    assert loaded == readings


def test_load_user_readings_converts_meter_id_to_int(
    tmp_path: Path, monkeypatch
) -> None:
    """Проверяет, что meter_id приводится к int при загрузке."""
    monkeypatch.setattr("storage.READINGS_FILE", str(tmp_path / "readings.json"))

    # Записываем файл вручную с meter_id как строкой.
    file_path = tmp_path / "readings.json"
    file_path.write_text(
        json.dumps({"test_user": [{"meter_id": "1", "value": 100.0}]}),
        encoding="utf-8",
    )

    loaded = load_user_readings("test_user")

    assert loaded[0]["meter_id"] == 1

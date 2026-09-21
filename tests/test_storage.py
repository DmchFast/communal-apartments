import json
from pathlib import Path

from models.meters import Meter
from models.readings import Reading
from storage import (
    load_user_meters,
    save_user_meters,
    load_user_readings,
    save_user_readings,
)


def test_save_and_load_user_meters(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        "storage.METERS_FILE", str(tmp_path / "meters.json")
    )
    meters = [
        Meter(1, "Вода", "м^3", None),
        Meter(2, "Газ", "м^3", 7.5),
    ]
    save_user_meters("test_user", meters)
    loaded = load_user_meters("test_user")
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].name == "Вода"
    assert loaded[1].tariff == 7.5


def test_load_user_meters_returns_empty_for_unknown_user(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "storage.METERS_FILE", str(tmp_path / "meters.json")
    )
    assert load_user_meters("unknown") == []


def test_save_and_load_user_readings(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "storage.READINGS_FILE", str(tmp_path / "readings.json")
    )
    readings = [
        Reading(1, 100.0, "2026-09-15", "10:00:00"),
        Reading(1, 150.0, "2026-09-16", "11:00:00"),
    ]
    save_user_readings("test_user", readings)
    loaded = load_user_readings("test_user")
    assert len(loaded) == 2
    assert loaded[0].meter_id == 1
    assert loaded[0].value == 100.0


def test_load_user_readings_converts_meter_id_to_int(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "storage.READINGS_FILE", str(tmp_path / "readings.json")
    )
    file_path = tmp_path / "readings.json"
    file_path.write_text(
        json.dumps(
            {"test_user": [{"meter_id": "1", "value": 100.0}]}
        ),
        encoding="utf-8",
    )
    loaded = load_user_readings("test_user")
    assert loaded[0].meter_id == 1

from models.readings import (
    add_reading,
    get_history,
    calculate_consumption,
    delete_reading,
)


def test_add_reading_adds_record_with_date_and_time(
    empty_readings: list,
) -> None:
    reading = add_reading(empty_readings, 1, 100.0)
    assert len(empty_readings) == 1
    assert reading.meter_id == 1
    assert reading.value == 100.0
    assert reading.date
    assert reading.time


def test_get_history_filters_by_meter_id(empty_readings: list) -> None:
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 2, 200.0)
    add_reading(empty_readings, 1, 150.0)
    history = get_history(empty_readings, 1)
    assert len(history) == 2
    assert all(r.meter_id == 1 for r in history)


def test_get_history_returns_empty_list_for_unknown_meter(
    empty_readings: list,
) -> None:
    add_reading(empty_readings, 1, 100.0)
    assert get_history(empty_readings, 999) == []


def test_calculate_consumption_returns_difference(
    empty_readings: list,
) -> None:
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 1, 150.0)
    consumption = calculate_consumption(empty_readings, 1)
    assert consumption == 50.0


def test_calculate_consumption_returns_none_for_insufficient_data(
    empty_readings: list,
) -> None:
    add_reading(empty_readings, 1, 100.0)
    assert calculate_consumption(empty_readings, 1) is None


def test_calculate_consumption_returns_none_for_empty_readings(
    empty_readings: list,
) -> None:
    assert calculate_consumption(empty_readings, 1) is None


def test_delete_reading_removes_by_index(empty_readings: list) -> None:
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 1, 150.0)
    add_reading(empty_readings, 1, 200.0)
    result = delete_reading(empty_readings, 1, 1)
    assert result is True
    history = get_history(empty_readings, 1)
    assert len(history) == 2
    assert history[1].value == 200.0


def test_delete_reading_returns_false_for_invalid_index(
    empty_readings: list,
) -> None:
    add_reading(empty_readings, 1, 100.0)
    assert delete_reading(empty_readings, 1, 5) is False
    assert len(empty_readings) == 1

from readings import add_reading, get_history, calculate_consumption


def test_add_reading_adds_record_with_date_and_time(empty_readings: list) -> None:
    """Проверяет, что add_reading добавляет запись с датой и временем."""
    record = add_reading(empty_readings, 1, 100.0)

    assert len(empty_readings) == 1
    assert record["meter_id"] == 1
    assert record["value"] == 100.0
    assert "date" in record
    assert "time" in record


def test_get_history_filters_by_meter_id(empty_readings: list) -> None:
    """Проверяет фильтрацию показаний по ID счётчика."""
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 2, 200.0)
    add_reading(empty_readings, 1, 150.0)

    history = get_history(empty_readings, 1)

    assert len(history) == 2
    assert all(r["meter_id"] == 1 for r in history)


def test_get_history_returns_empty_list_for_unknown_meter(empty_readings: list) -> None:
    """Проверяет, что для неизвестного счётчика возвращается пустой список."""
    add_reading(empty_readings, 1, 100.0)

    assert get_history(empty_readings, 999) == []


def test_calculate_consumption_returns_difference(empty_readings: list) -> None:
    """Проверяет расчёт расхода между двумя последними показаниями."""
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 1, 150.0)

    consumption = calculate_consumption(empty_readings, 1)

    assert consumption == 50.0


def test_calculate_consumption_returns_none_for_insufficient_data(empty_readings: list) -> None:
    """Проверяет, что при одном показании расход не вычисляется."""
    add_reading(empty_readings, 1, 100.0)

    assert calculate_consumption(empty_readings, 1) is None


def test_calculate_consumption_returns_none_for_empty_readings(empty_readings: list) -> None:
    """Проверяет, что при пустом списке показаний расход не вычисляется."""
    assert calculate_consumption(empty_readings, 1) is None
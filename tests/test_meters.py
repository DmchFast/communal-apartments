from meters import add_meter, list_meters


def test_add_meter_assigns_sequential_ids(empty_meters: dict) -> None:
    """Проверяет, что add_meter присваивает последовательные ID."""
    id1 = add_meter(empty_meters, "Вода", "м^3")
    id2 = add_meter(empty_meters, "Электричество", "кВт*ч")

    assert id1 == 1
    assert id2 == 2
    assert len(empty_meters) == 2


def test_add_meter_stores_correct_data(empty_meters: dict) -> None:
    """Проверяет, что данные счётчика сохраняются корректно."""
    meter_id = add_meter(empty_meters, "Газ", "м^3")
    meter = empty_meters[meter_id]

    assert meter["name"] == "Газ"
    assert meter["unit"] == "м^3"
    assert meter["tariff"] is None


def test_list_meters_outputs_all_meters(capsys, empty_meters: dict) -> None:
    """Проверяет, что list_meters выводит все счётчики."""
    add_meter(empty_meters, "Вода", "м^3")
    add_meter(empty_meters, "Газ", "м^3")

    list_meters(empty_meters)
    captured = capsys.readouterr()

    assert "[1] Вода (м^3)" in captured.out
    assert "[2] Газ (м^3)" in captured.out


def test_list_meters_shows_no_meters_message(capsys) -> None:
    """Проверяет сообщение при пустом словаре счётчиков."""
    list_meters({})
    captured = capsys.readouterr()

    assert "Счётчиков пока нет." in captured.out
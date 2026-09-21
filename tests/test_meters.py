from models.meters import add_meter, list_meters, delete_meter


def test_add_meter_assigns_sequential_ids(empty_meters: list) -> None:
    meter1 = add_meter(empty_meters, "Вода", "м^3")
    meter2 = add_meter(empty_meters, "Электричество", "кВт*ч")
    assert meter1.id == 1
    assert meter2.id == 2
    assert len(empty_meters) == 2


def test_add_meter_stores_correct_data(empty_meters: list) -> None:
    meter = add_meter(empty_meters, "Газ", "м^3")
    assert meter.name == "Газ"
    assert meter.unit == "м^3"
    assert meter.tariff is None


def test_list_meters_outputs_all_meters(capsys, empty_meters: list) -> None:
    add_meter(empty_meters, "Вода", "м^3")
    add_meter(empty_meters, "Газ", "м^3")
    list_meters(empty_meters)
    captured = capsys.readouterr()
    assert "[1] Вода (м^3)" in captured.out
    assert "[2] Газ (м^3)" in captured.out


def test_list_meters_shows_no_meters_message(capsys) -> None:
    list_meters([])
    captured = capsys.readouterr()
    assert "Счётчиков пока нет." in captured.out


def test_delete_meter_removes_existing(empty_meters: list) -> None:
    meter = add_meter(empty_meters, "Вода", "м^3")
    result = delete_meter(empty_meters, meter.id)
    assert result is True
    assert len(empty_meters) == 0


def test_delete_meter_returns_false_for_unknown(empty_meters: list) -> None:
    assert delete_meter(empty_meters, 999) is False

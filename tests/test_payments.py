from models.meters import add_meter
from models.readings import Reading, add_reading
from models.payments import Payment, create_payment


def test_create_payment_returns_correct_amount(
    empty_meters: list,
    empty_readings: list,
) -> None:
    """Платёж считается как расход × тариф."""
    meter = add_meter(empty_meters, "Вода", "м^3")
    meter.set_tariff(45.5)

    add_reading(empty_readings, meter.id, 100.0, meter)
    add_reading(empty_readings, meter.id, 150.0, meter)

    payment = create_payment(empty_readings, meter.id)

    assert payment is not None
    assert payment.consumption == 50.0
    assert payment.tariff == 45.5
    assert payment.amount == 2275.0
    assert payment.meter is meter


def test_create_payment_returns_none_without_two_readings(
    empty_meters: list,
    empty_readings: list,
) -> None:
    meter = add_meter(empty_meters, "Вода", "м^3")
    add_reading(empty_readings, meter.id, 100.0, meter)

    assert create_payment(empty_readings, meter.id) is None


def test_create_payment_uses_meter_object_from_readings(
    empty_readings: list,
) -> None:
    add_reading(empty_readings, 1, 100.0)
    add_reading(empty_readings, 1, 150.0)

    payment = create_payment(empty_readings, 1)

    assert payment is not None
    assert payment.meter.id == 1


def test_payment_rejects_negative_consumption(empty_meters: list) -> None:
    meter = add_meter(empty_meters, "Вода", "м^3")
    previous = Reading(meter, 150.0)
    current = Reading(meter, 100.0)

    try:
        Payment(current, previous)
    except ValueError as error:
        assert "меньше предыдущего" in str(error)
    else:
        raise AssertionError("Ожидалась ошибка отрицательного расхода")


def test_payment_rejects_readings_from_different_meters(
    empty_meters: list,
) -> None:
    first_meter = add_meter(empty_meters, "Вода", "м^3")
    second_meter = add_meter(empty_meters, "Газ", "м^3")

    try:
        Payment(Reading(second_meter, 150.0), Reading(first_meter, 100.0))
    except ValueError as error:
        assert "разным счётчикам" in str(error)
    else:
        raise AssertionError("Ожидалась ошибка разных счётчиков")


def test_payment_without_tariff_has_no_amount(
    empty_meters: list,
    empty_readings: list,
) -> None:
    meter = add_meter(empty_meters, "Газ", "м^3")  # тариф не установлен

    add_reading(empty_readings, meter.id, 10.0, meter)
    add_reading(empty_readings, meter.id, 20.0, meter)

    payment = create_payment(empty_readings, meter.id)

    assert payment is not None
    assert payment.consumption == 10.0
    assert payment.tariff is None
    assert payment.amount is None


def test_payment_str_contains_meter_name(
    empty_meters: list,
    empty_readings: list,
) -> None:
    meter = add_meter(empty_meters, "Электричество", "кВт*ч")
    meter.set_tariff(5.0)

    add_reading(empty_readings, meter.id, 100.0, meter)
    add_reading(empty_readings, meter.id, 200.0, meter)

    payment = create_payment(empty_readings, meter.id)
    assert payment is not None
    assert "Электричество" in str(payment)

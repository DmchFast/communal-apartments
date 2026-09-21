from models.meters import add_meter
from models.tariffs import set_tariff, calculate_payment


def test_set_tariff_updates_meter(empty_meters: list) -> None:
    meter = add_meter(empty_meters, "Вода", "м^3")
    set_tariff(empty_meters, meter.id, 45.5)
    assert meter.tariff == 45.5


def test_calculate_payment_returns_correct_amount() -> None:
    payment = calculate_payment(50.0, 45.5)
    assert payment == 2275.0


def test_calculate_payment_rounds_to_two_decimals() -> None:
    payment = calculate_payment(33.333, 10.0)
    assert payment == 333.33


def test_calculate_payment_zero_consumption() -> None:
    assert calculate_payment(0.0, 45.5) == 0.0

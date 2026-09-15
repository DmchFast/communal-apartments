from tariffs import set_tariff, calculate_payment
from meters import add_meter


def test_set_tariff_updates_meter(empty_meters: dict) -> None:
    """Проверяет установку тарифа для счётчика."""
    meter_id = add_meter(empty_meters, "Вода", "м^3")
    set_tariff(empty_meters, meter_id, 45.5)

    assert empty_meters[meter_id]["tariff"] == 45.5


def test_calculate_payment_returns_correct_amount() -> None:
    """Проверяет корректность расчёта платежа."""
    payment = calculate_payment(50.0, 45.5)

    assert payment == 2275.0


def test_calculate_payment_rounds_to_two_decimals() -> None:
    """Проверяет округление результата до двух знаков."""
    payment = calculate_payment(33.333, 10.0)

    assert payment == 333.33


def test_calculate_payment_zero_consumption() -> None:
    """Проверяет, что при нулевом расходе платёж равен нулю."""
    assert calculate_payment(0.0, 45.5) == 0.0
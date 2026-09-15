from typing import Any


def set_tariff(
    meters: dict[int, dict[str, Any]], meter_id: int, tariff: float
) -> None:
    # Установка тарифа для счётчика.
    meters[meter_id]["tariff"] = tariff


def calculate_payment(consumption: float, tariff: float) -> float:
    # Вычисление стоимости (расход * тариф).
    return round(consumption * tariff, 2)

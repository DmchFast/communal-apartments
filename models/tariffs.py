from models.meters import Meter


def set_tariff(meters: list[Meter], meter_id: int, tariff: float | None) -> bool:
    """Установить тариф для счётчика."""
    for meter in meters:
        if meter.id == meter_id:
            meter.set_tariff(tariff)
            return True
    return False


def calculate_payment(consumption: float, tariff: float) -> float:
    """Вычислить платёж."""
    return round(consumption * tariff, 2)

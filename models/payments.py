from __future__ import annotations

from models.meters import Meter
from models.readings import Reading, get_history


class Payment:
    """Платёж за показания счётчика."""

    def __init__(
        self,
        current: Reading,
        previous: Reading | None = None,
        meter: Meter | None = None,
    ) -> None:
        self.current = current
        self.previous = previous
        self.meter = meter or current.meter

        if current.meter.id != self.meter.id:
            raise ValueError("Текущее показание относится к другому счётчику")
        if previous is not None and previous.meter.id != self.meter.id:
            raise ValueError("Показания относятся к разным счётчикам")

        self.consumption: float | None = None
        if previous is not None:
            self.consumption = current.value - previous.value
            if self.consumption < 0:
                raise ValueError(
                    "Текущее показание не может быть меньше предыдущего"
                )

        self.tariff: float | None = self.meter.tariff
        self.amount: float | None = None
        if self.consumption is not None and self.tariff is not None:
            self.amount = round(self.consumption * self.tariff, 2)

    def __str__(self) -> str:
        if self.amount is None:
            return f"Платёж по счётчику «{self.meter.name}»: недостаточно данных"
        return (
            f"Платёж по счётчику «{self.meter.name}»: "
            f"расход {self.consumption:.2f} {self.meter.unit} × "
            f"тариф {self.tariff:.2f} руб. = {self.amount:.2f} руб."
        )


def create_payment(readings: list[Reading], meter_id: int) -> Payment | None:
    """Создать платёж по последним двум показаниям счётчика."""
    history = get_history(readings, meter_id)
    if len(history) < 2:
        return None
    return Payment(history[-1], history[-2])

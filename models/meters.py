from typing import Any


class Meter:
    """Счётчик коммунального ресурса."""

    def __init__(
        self,
        meter_id: int,
        name: str,
        unit: str,
        tariff: float | None = None,
    ) -> None:
        self.id = meter_id
        self.name = name
        self.unit = unit
        self.tariff = tariff

    def __str__(self) -> str:
        if self.tariff is not None:
            tariff_str = f", тариф: {self.tariff:.2f} руб."
        else:
            tariff_str = ", тариф не установлен"
        return f"[{self.id}] {self.name} ({self.unit}){tariff_str}"

    def set_tariff(self, tariff: float | None) -> None:
        """Установить тариф. None сбрасывает тариф."""
        self.tariff = tariff

    @classmethod
    def from_data(cls, meter_id: int, data: dict[str, Any]) -> "Meter":
        """Создать объект из данных JSON."""
        return cls(
            meter_id=meter_id,
            name=data["name"],
            unit=data["unit"],
            tariff=data.get("tariff"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать объект в данные для JSON."""
        return {
            "name": self.name,
            "unit": self.unit,
            "tariff": self.tariff,
        }


def add_meter(meters: list[Meter], name: str, unit: str) -> Meter:
    """Добавить счётчик в коллекцию."""
    meter_id = max((m.id for m in meters), default=0) + 1
    meter = Meter(meter_id, name, unit)
    meters.append(meter)
    return meter


def delete_meter(meters: list[Meter], meter_id: int) -> bool:
    """Удалить счётчик по ID."""
    for i, meter in enumerate(meters):
        if meter.id == meter_id:
            del meters[i]
            return True
    return False


def list_meters(meters: list[Meter]) -> None:
    """Вывести список счётчиков."""
    if not meters:
        print("Счётчиков пока нет.")
        return
    for meter in meters:
        print(meter)

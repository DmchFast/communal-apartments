from typing import Any


def add_meter(meters: dict[int, dict[str, Any]], name: str, unit: str) -> int:
    '''Добавление счётчика в словарь meters с возвратом присвоенного ID.'''
    meter_id = max(meters.keys(), default=0) + 1
    meters[meter_id] = {"name": name, "unit": unit, "tariff": None}
    return meter_id


def delete_meter(meters: dict[int, dict[str, Any]], meter_id: int) -> bool:
    '''Удаление счётчика по ID, True -> счётчик был удалён.'''
    if meter_id in meters:
        del meters[meter_id]
        return True
    return False


def list_meters(meters: dict[int, dict[str, Any]]) -> None:
    '''Вывод списка счётчиков.'''
    if not meters:
        print("Счётчиков пока нет.")
        return
    for meter_id, data in meters.items():
        tariff = data.get("tariff")
        tariff_str = (
            f", тариф: {tariff:.2f} руб."
            if tariff is not None
            else ", тариф не установлен"
        )
        print(f"[{meter_id}] {data['name']} ({data['unit']}){tariff_str}")

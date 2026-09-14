def add_meter(meters: dict[int, dict], name: str, unit: str) -> int:
    #Добавление счётчика в словарь meters. с возвратом присвоенного ID
    meter_id = max(meters.keys(), default=0) + 1
    meters[meter_id] = {"name": name, "unit": unit, "tariff": 0.0}
    return meter_id


def list_meters(meters: dict[int, dict]) -> None:
    #Вывод список счётчиков
    if not meters:
        print("Счётчиков пока нет.")
        return
    for meter_id, data in meters.items():
        print(f"[{meter_id}] {data['name']} ({data['unit']})")
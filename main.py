import math

from meters import add_meter, list_meters
from storage import load_json, save_json
from utils import input_float
from readings import add_reading, get_history, calculate_consumption
from tariffs import set_tariff, calculate_payment

READINGS_FILE = "data/readings.json"
METERS_FILE = "data/meters.json"


def load_meters() -> dict[int, dict]:
    stored_meters = load_json(METERS_FILE) or {}
    return {int(meter_id): data for meter_id, data in stored_meters.items()}


def load_readings() -> list[dict]:
    stored_readings = load_json(READINGS_FILE) or []
    for reading in stored_readings:
        reading["meter_id"] = int(reading["meter_id"])
    return stored_readings


def get_user() -> str:
    return input("Введите имя пользователя: ")


def show_menu() -> None:
    print("\n=== Учёт показаний коммунальных счётчиков ===")
    print("1. Показать счётчики")
    print("2. Добавить счётчик")
    print("3. Внести показание")
    print("4. История показаний")
    print("5. Рассчитать расход")
    print("6. Установить тариф")
    print("7. Рассчитать платёж")
    print("0. Выход")


def handle_set_tariff(meters: dict) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    if meter_id not in meters:
        print("Счётчик не найден.")
        return

    tariff_input = input("Тариф (руб. за единицу) [оставьте пустым, чтобы не устанавливать]: ").strip()
    if not tariff_input:
        print("Тариф не установлен.")
        return

    try:
        tariff = float(tariff_input)
    except ValueError:
        print("Ошибка: тариф должен быть числом.")
        return

    set_tariff(meters, meter_id, tariff)
    save_json(METERS_FILE, meters)
    print("Тариф установлен.")


def handle_show_payment(meters: dict, readings: list[dict]) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    consumption = calculate_consumption(readings, meter_id)
    if consumption is None:
        print("Недостаточно данных для расчёта.")
        return
    tariff = meters[meter_id].get("tariff", 0.0)
    payment = calculate_payment(consumption, tariff)
    print(
        f"Расход: {consumption:.2f}, тариф: {tariff:.2f}, "
        f"к оплате: {payment:.2f} руб."
    )


def handle_show_consumption(meters: dict, readings: list[dict]) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    consumption = calculate_consumption(readings, meter_id)
    if consumption is None:
        print("Недостаточно данных (нужно минимум два показания).")
        return
    if consumption < 0:
        print("Внимание: текущее показание меньше предыдущего.")
        return
    print(f"Расход: {consumption:.2f}")


def handle_add_reading(meters: dict, readings: list[dict]) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    if meter_id not in meters:
        print("Счётчик с таким ID не найден.")
        return

    value = input_float("Текущее показание: ")
    if not math.isfinite(value) or value < 0:
        print("Ошибка: показание должно быть неотрицательным числом.")
        return
    history = get_history(readings, meter_id)
    if history and value < history[-1]["value"]:
        print("Ошибка: новое показание не может быть меньше предыдущего.")
        return
    add_reading(readings, meter_id, value)
    save_json(READINGS_FILE, readings)
    print("Показание сохранено.")


def handle_show_history(meters: dict, readings: list[dict]) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    history = get_history(readings, meter_id)
    if not history:
        print("Показаний по этому счётчику нет.")
        return
    for r in history:
        print(f"{r['date']} {r['time']} — {r['value']}")


def handle_add_meter(meters: dict) -> None:
    name = input("Название счётчика: ").strip()
    if not name:
        print("Ошибка: название счётчика не может быть пустым.")
        return
    unit = input("Единица измерения (кВт*ч, м^3 и т.п.): ").strip()
    if not unit:
        print("Ошибка: единица измерения не может быть пустой.")
        return
    add_meter(meters, name, unit)
    save_json(METERS_FILE, meters)


def main() -> None:
    user = get_user()
    print(f"\nЗдравствуйте, {user}!")

    meters = load_meters()
    readings = load_readings()

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_meters(meters)
        elif choice == "2":
            handle_add_meter(meters)
        elif choice == "3":
            handle_add_reading(meters, readings)
        elif choice == "4":
            handle_show_history(meters, readings)
        elif choice == "5":
            handle_show_consumption(meters, readings)
        elif choice == "6":
            handle_set_tariff(meters)
        elif choice == "7":
            handle_show_payment(meters, readings)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


main()
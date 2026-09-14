from meters import add_meter, list_meters
from storage import load_json, save_json
from utils import input_float
from readings import add_reading, get_history
from readings import add_reading, get_history, calculate_consumption

READINGS_FILE = "data/readings.json"
METERS_FILE = "data/meters.json"


def get_user() -> str:
    return input("Введите имя пользователя: ")


def show_menu() -> None:
    print("\n=== Учёт показаний коммунальных счётчиков ===")
    print("1. Показать счётчики")
    print("2. Добавить счётчик")
    print("3. Внести показание")
    print("4. История показаний")
    print("0. Выход")


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
    name = input("Название счётчика: ")
    unit = input("Единица измерения (кВт·ч, м³ и т.п.): ")
    add_meter(meters, name, unit)
    save_json(METERS_FILE, meters)


def main() -> None:
    user = get_user()
    print(f"\nЗдравствуйте, {user}!")

    meters = load_json(METERS_FILE) or {}
    readings = load_json(READINGS_FILE) or []

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
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


main()
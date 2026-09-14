from meters import add_meter, list_meters
from storage import load_json, save_json
from utils import input_float

METERS_FILE = "data/meters.json"


def get_user() -> str:
    return input("Введите имя пользователя: ")


def show_menu() -> None:
    print("\n=== Учёт показаний коммунальных счётчиков ===")
    print("1. Показать счётчики")
    print("2. Добавить счётчик")
    print("0. Выход")


def handle_add_meter(meters: dict) -> None:
    name = input("Название счётчика: ")
    unit = input("Единица измерения (кВт·ч, м³ и т.п.): ")
    add_meter(meters, name, unit)
    save_json(METERS_FILE, meters)


def main() -> None:
    user = get_user()
    print(f"\nЗдравствуйте, {user}!")

    meters = load_json(METERS_FILE) or {}

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_meters(meters)
        elif choice == "2":
            handle_add_meter(meters)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


main()
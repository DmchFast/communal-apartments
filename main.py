import math
from typing import Any

from meters import add_meter, list_meters
from storage import (
    load_user_meters,
    save_user_meters,
    load_user_readings,
    save_user_readings,
)
from utils import input_float
from readings import add_reading, get_history, calculate_consumption
from tariffs import set_tariff, calculate_payment


def get_user() -> str:
    return input("Введите имя пользователя: ")


def show_menu() -> None:
    print("=== Учёт показаний коммунальных счётчиков ===")
    print("1. Показать счётчики")
    print("2. Добавить счётчик")
    print("3. Внести показание")
    print("4. История показаний")
    print("5. Рассчитать расход")
    print("6. Установить тариф")
    print("7. Рассчитать платёж")
    print("0. Выход")


def handle_set_tariff(meters: dict[int, dict[str, Any]]) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    if meter_id not in meters:
        print("Счётчик не найден.")
        return

    tariff_input = input(
        "Тариф (руб. за единицу) [пусто или пробел - сброс тарифа]: "
    ).strip()

    if not tariff_input:
        meters[meter_id]["tariff"] = None
        print("Тариф сброшен (не установлен).")
        return

    try:
        tariff = float(tariff_input)
    except ValueError:
        print("Ошибка: тариф должен быть числом.")
        return

    if tariff < 0:
        print("Ошибка: тариф не может быть отрицательным.")
        return

    set_tariff(meters, meter_id, tariff)
    print("Тариф установлен.")


def handle_show_payment(
    meters: dict[int, dict[str, Any]], readings: list[dict[str, Any]]
) -> None:
    list_meters(meters)
    try:
        meter_id = int(input("ID счётчика: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    consumption = calculate_consumption(readings, meter_id)
    if consumption is None:
        print("Недостаточно данных для расчёта (нужно минимум два показания).")
        return

    tariff = meters[meter_id].get("tariff")
    if tariff is None:
        print("Тариф не установлен. Установите тариф через пункт 6.")
        return

    payment = calculate_payment(consumption, tariff)
    print(f"К оплате: {payment:.2f} руб.")


def handle_show_consumption(
    meters: dict[int, dict[str, Any]], readings: list[dict[str, Any]]
) -> None:
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


def handle_add_reading(
    meters: dict[int, dict[str, Any]], readings: list[dict[str, Any]]
) -> None:
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
    print("Показание сохранено.")


def handle_show_history(
    meters: dict[int, dict[str, Any]], readings: list[dict[str, Any]]
) -> None:
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
        print(f"{r['date']} {r['time']} - {r['value']}")


def handle_add_meter(meters: dict[int, dict[str, Any]]) -> None:
    name = input("Название счётчика: ").strip()
    if not name:
        print("Ошибка: название счётчика не может быть пустым.")
        return
    unit = input("Единица измерения (кВт*ч, м^3 и т.п.): ").strip()
    if not unit:
        print("Ошибка: единица измерения не может быть пустой.")
        return
    add_meter(meters, name, unit)


def main() -> None:
    user = get_user()
    print(f"\nЗдравствуйте, {user}!\n")

    meters = load_user_meters(user)
    readings = load_user_readings(user)

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()
        print("================================")
        if choice == "1":
            list_meters(meters)
        elif choice == "2":
            handle_add_meter(meters)
            save_user_meters(user, meters)
        elif choice == "3":
            handle_add_reading(meters, readings)
            save_user_readings(user, readings)
        elif choice == "4":
            handle_show_history(meters, readings)
        elif choice == "5":
            handle_show_consumption(meters, readings)
        elif choice == "6":
            handle_set_tariff(meters)
            save_user_meters(user, meters)
        elif choice == "7":
            handle_show_payment(meters, readings)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


main()

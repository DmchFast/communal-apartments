from datetime import datetime
from utils import input_float


def get_user():
    name = input("Введите имя пользователя: ")
    return name


def get_meter_data():
    name = input("Название счётчика: ")
    prev = input_float("Предыдущее показание: ")
    curr = input_float("Текущее показание: ")
    return name, prev, curr


def calculate_consumption(prev, curr):
    if curr < prev:
        return None
    return curr - prev


def main():
    print("=== Учёт показаний коммунальных счётчиков ===\n")
    user = get_user()
    meter_name, previous, current = get_meter_data()

    consumption = calculate_consumption(previous, current)
    if consumption is None:
        print("Ошибка: текущее показание не может быть меньше предыдущего.")
        return

    today = datetime.now().date().strftime("%d.%m.%Y")

    print("\n--- Результат ---")
    print(f"Пользователь: {user}")
    print(f"Счётчик: {meter_name}")
    print(f"Предыдущее показание: {previous:.2f}")
    print(f"Текущее показание: {current:.2f}")
    print(f"Расход: {consumption:.2f}")
    print(f"Дата снятия: {today}")


main()
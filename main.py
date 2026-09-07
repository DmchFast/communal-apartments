from datetime import datetime

def main():
    print("=== Учёт показаний коммунальных счётчиков ===\n")

    meter_name = input("Название счётчика: ")
    previous = float(input("Предыдущее показание: "))
    current = float(input("Текущее показание: "))

    if current < previous:
        print("Ошибка: текущее показание не может быть меньше предыдущего.")
        return

    consumption = current - previous
    today = datetime.now().date().strftime("%d.%m.%Y")

    print("\n--- Результат ---")
    print(f"Счётчик: {meter_name}")
    print(f"Предыдущее показание: {previous:.2f}")
    print(f"Текущее показание: {current:.2f}")
    print(f"Расход: {consumption:.2f}")
    print(f"Дата снятия: {today}")

main()
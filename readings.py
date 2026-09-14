from datetime import datetime


def add_reading(readings: list[dict], meter_id: int, value: float) -> dict:
    #Показания с текущей датой и временем
    now = datetime.now()
    record = {
        "meter_id": meter_id,
        "value": value,
        "date": now.date().isoformat(),
        "time": now.time().strftime("%H:%M:%S"),
    }
    readings.append(record)
    return record


def get_history(readings: list[dict], meter_id: int) -> list[dict]:
    return [r for r in readings if r["meter_id"] == meter_id]
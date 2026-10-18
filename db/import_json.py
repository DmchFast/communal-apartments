import json
from db.database import get_connection

METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"

def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def import_users_and_meters(conn):
    meters_data = load_json(METERS_FILE) or {}
    users = []
    meters = []
    user_id = 0
    meter_id = 0

    for username, user_meters in meters_data.items():
        user_id += 1
        users.append((user_id, username))
        for old_meter_id, meter_info in user_meters.items():
            meter_id += 1
            meters.append((
                meter_id,
                user_id,
                meter_info["name"],
                meter_info["unit"],
                meter_info.get("tariff"),
            ))

    conn.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?)",
        users,
    )
    conn.executemany(
        "INSERT INTO meters (id, user_id, name, unit, tariff) VALUES (?, ?, ?, ?, ?)",
        meters,
    )
    return meter_id

def import_readings(conn):
    readings_data = load_json(READINGS_FILE) or {}
    readings = []
    reading_id = 0

    for username, user_readings in readings_data.items():
        for item in user_readings:
            reading_id += 1
            readings.append((
                reading_id,
                item["meter_id"],
                item["value"],
                item["date"],
                item["time"],
            ))

    conn.executemany(
        "INSERT INTO readings (id, meter_id, value, date, time) VALUES (?, ?, ?, ?, ?)",
        readings,
    )

def main():
    conn = get_connection()
    try:
        # Очищаем таблицы перед импортом (удаляет старые данные)
        conn.execute("DELETE FROM readings")
        conn.execute("DELETE FROM meters")
        conn.execute("DELETE FROM users")
        import_users_and_meters(conn)
        import_readings(conn)
        conn.commit()
        print("Импорт завершён.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
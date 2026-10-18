-- =============================================
-- Communal Apartments: структура базы данных
-- =============================================

CREATE TABLE IF NOT EXISTS users (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS meters (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name    TEXT NOT NULL,
    unit    TEXT NOT NULL,
    tariff  REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS readings (
    id       INTEGER PRIMARY KEY,
    meter_id INTEGER NOT NULL,
    value    REAL NOT NULL,
    date     TEXT NOT NULL,
    time     TEXT NOT NULL,
    FOREIGN KEY (meter_id) REFERENCES meters(id)
);
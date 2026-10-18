-- Список всех счётчиков с именами пользователей (JOIN)
SELECT meters.id, meters.name AS meter_name, meters.unit,
       meters.tariff, users.name AS user_name
FROM meters
JOIN users ON meters.user_id = users.id
ORDER BY users.name, meters.name;

-- Счётчики без установленного тарифа (WHERE IS NULL)
SELECT id, name, unit
FROM meters
WHERE tariff IS NULL;

-- Показания по конкретному счётчику (WHERE + параметр)
SELECT id, value, date, time
FROM readings
WHERE meter_id = ?
ORDER BY date, time;

-- Все показания с названием счётчика (JOIN)
SELECT readings.id, readings.value, readings.date, readings.time,
       meters.name AS meter_name, meters.unit
FROM readings
JOIN meters ON readings.meter_id = meters.id
ORDER BY readings.date, readings.time;

-- Количество счётчиков у каждого пользователя (GROUP BY + COUNT)
SELECT users.name AS user_name, COUNT(meters.id) AS meters_count
FROM users
LEFT JOIN meters ON users.id = meters.user_id
GROUP BY users.id, users.name
ORDER BY meters_count DESC;

-- Количество показаний по каждому счётчику (GROUP BY + COUNT)
SELECT meters.name AS meter_name, COUNT(readings.id) AS readings_count
FROM meters
LEFT JOIN readings ON meters.id = readings.meter_id
GROUP BY meters.id, meters.name
ORDER BY readings_count DESC;

-- Средний расход (разница между соседними показаниями) по счётчику
SELECT meter_id,
       MIN(value) AS min_value,
       MAX(value) AS max_value,
       AVG(value) AS avg_value,
       COUNT(*) AS readings_count
FROM readings
GROUP BY meter_id
HAVING COUNT(*) >= 2;

-- Счётчики, у которых более одного показания (HAVING)
SELECT meters.name AS meter_name, COUNT(readings.id) AS readings_count
FROM meters
JOIN readings ON meters.id = readings.meter_id
GROUP BY meters.id, meters.name
HAVING COUNT(readings.id) > 1
ORDER BY readings_count DESC;

-- Пользователи, у которых есть счётчики с тарифом (WHERE + JOIN)
SELECT DISTINCT users.name
FROM users
JOIN meters ON users.id = meters.user_id
WHERE meters.tariff IS NOT NULL;

-- Последнее показание по каждому счётчику (подзапрос с MAX(date))
SELECT meters.name AS meter_name,
       readings.value,
       readings.date,
       readings.time
FROM meters
JOIN readings ON meters.id = readings.meter_id
WHERE readings.date = (
    SELECT MAX(r2.date)
    FROM readings r2
    WHERE r2.meter_id = meters.id
)
ORDER BY meters.name;

-- Суммарный расход по счётчику SUM(next.value - current.value) через self-join
SELECT m.name AS meter_name,
       SUM(r2.value - r1.value) AS total_consumption
FROM meters m
JOIN readings r1 ON m.id = r1.meter_id
JOIN readings r2 ON m.id = r2.meter_id AND r2.date > r1.date
GROUP BY m.id, m.name;

-- Показания за период
SELECT id, meter_id, value, date, time
FROM readings
WHERE date BETWEEN ? AND ?
ORDER BY date, time;
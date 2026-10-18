from django.shortcuts import render
from db.database import get_connection


def payments(request):
    conn = get_connection()
    meters = conn.execute("""
        SELECT id, name, unit, tariff
        FROM meters
        ORDER BY name
    """).fetchall()

    items = []
    for meter in meters:
        readings = conn.execute("""
            SELECT value, date, time
            FROM readings
            WHERE meter_id = ?
            ORDER BY date, time DESC
            LIMIT 2
        """, (meter["id"],)).fetchall()

        if len(readings) < 2:
            continue

        curr = readings[0]
        prev = readings[1]
        consumption = curr["value"] - prev["value"]
        if consumption < 0:
            continue

        amount = None
        amount_str = "тариф не установлен"
        if meter["tariff"] is not None:
            amount = round(consumption * meter["tariff"], 2)
            amount_str = f"{amount:.2f} руб."

        items.append({
            "meter": meter,
            "consumption": consumption,
            "amount_str": amount_str,
        })

    conn.close()
    return render(request, "payments/payment_list.html", {"items": items})


def payment_detail(request, meter_id):
    conn = get_connection()
    meter = conn.execute("""
        SELECT id, name, unit, tariff
        FROM meters
        WHERE id = ?
    """, (meter_id,)).fetchone()

    if meter is None:
        conn.close()
        return render(
            request, "payments/payment_detail.html", {"meter": None}, status=404
        )

    readings = conn.execute("""
        SELECT value, date, time
        FROM readings
        WHERE meter_id = ?
        ORDER BY date, time DESC
        LIMIT 2
    """, (meter_id,)).fetchall()

    payment = None
    if len(readings) >= 2:
        curr = readings[0]
        prev = readings[1]
        consumption = curr["value"] - prev["value"]
        if consumption >= 0:
            amount = None
            if meter["tariff"] is not None:
                amount = round(consumption * meter["tariff"], 2)
            payment = {
                "consumption": consumption,
                "tariff": meter["tariff"],
                "amount": amount,
            }

    conn.close()
    return render(request, "payments/payment_detail.html", {
        "meter": meter,
        "payment": payment,
    })

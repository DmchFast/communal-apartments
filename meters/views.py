from django.shortcuts import render
from db.database import get_connection

def meters(request):
    conn = get_connection()
    rows = conn.execute("""
        SELECT meters.id, meters.name, meters.unit, meters.tariff,
               users.name AS user_name
        FROM meters
        JOIN users ON meters.user_id = users.id
        ORDER BY users.name, meters.name
    """).fetchall()
    conn.close()
    return render(request, "meters/meter_list.html", {"meters": rows})

def meter_detail(request, meter_id):
    conn = get_connection()
    meter = conn.execute("""
        SELECT meters.id, meters.name, meters.unit, meters.tariff,
               users.name AS user_name
        FROM meters
        JOIN users ON meters.user_id = users.id
        WHERE meters.id = ?
    """, (meter_id,)).fetchone()

    if meter is None:
        conn.close()
        return render(request, "meters/meter_detail.html", {"meter": None}, status=404)

    history = conn.execute("""
        SELECT id, value, date, time
        FROM readings
        WHERE meter_id = ?
        ORDER BY date, time
    """, (meter_id,)).fetchall()

    # Расчёт расхода и платежа по последним двум показаниям
    payment = None
    if len(history) >= 2:
        prev = history[-2]
        curr = history[-1]
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
    return render(request, "meters/meter_detail.html", {
        "meter": meter,
        "history": history,
        "payment": payment,
    })
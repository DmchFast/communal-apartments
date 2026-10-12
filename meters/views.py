from django.shortcuts import render
from models.meters import Meter
from models.readings import Reading, get_history
from models.payments import create_payment
from storage import METERS_FILE, READINGS_FILE, load_json


def _all_meters():
    """Загрузить счётчики всех пользователей."""
    all_data = load_json(METERS_FILE) or {}
    result = []
    for user_meters in all_data.values():
        for meter_id, data in user_meters.items():
            result.append(Meter.from_data(int(meter_id), data))
    return result


def _all_readings(meters):
    """Загрузить все показания и привязать к переданным Meter."""
    all_data = load_json(READINGS_FILE) or {}
    meters_by_id = {m.id: m for m in meters}
    result = []
    for user_readings in all_data.values():
        for item in user_readings:
            reading = Reading.from_data(item)
            meter = meters_by_id.get(reading.meter_id)
            if meter is not None:
                reading.meter = meter
                reading.meter_id = meter.id
                result.append(reading)
    return result


def meters(request):
    meters_list = _all_meters()
    return render(request, "meters/meter_list.html", {"meters": meters_list})


def meter_detail(request, meter_id):
    meters_list = _all_meters()
    meter = next((m for m in meters_list if m.id == meter_id), None)
    if meter is None:
        return render(request, "meters/meter_detail.html", {"meter": None}, status=404)

    readings_list = _all_readings(meters_list)
    history = get_history(readings_list, meter_id)
    payment = create_payment(readings_list, meter_id)

    context = {
        "meter": meter,
        "history": history,
        "payment": payment,
    }
    return render(request, "meters/meter_detail.html", context)
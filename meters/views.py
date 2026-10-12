from django.shortcuts import render
from models.meters import Meter
from storage import METERS_FILE, load_json

def _all_meters():
    """Загрузить счётчики всех пользователей."""
    all_data = load_json(METERS_FILE) or {}
    result = []
    for user_meters in all_data.values():
        for meter_id, data in user_meters.items():
            result.append(Meter.from_data(int(meter_id), data))
    return result

def meters(request):
    meters_list = _all_meters()
    return render(request, "meters/meter_list.html", {"meters": meters_list})
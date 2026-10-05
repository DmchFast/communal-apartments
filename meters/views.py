from django.http import HttpResponse

from homepage.views import page
from models.meters import Meter
from models.payments import create_payment
from models.readings import Reading, get_history
from storage import (
    METERS_FILE,
    READINGS_FILE,
    load_json,
)


def _all_meters() -> list[Meter]:
    """Загрузить счётчики всех пользователей (демо без авторизации)."""
    all_data = load_json(METERS_FILE) or {}
    result: list[Meter] = []
    for user_meters in all_data.values():
        for meter_id, data in user_meters.items():
            result.append(Meter.from_data(int(meter_id), data))
    return result


def _all_readings(meters: list[Meter]) -> list[Reading]:
    """Загрузить все показания и привязать к переданным Meter."""
    all_data = load_json(READINGS_FILE) or {}
    meters_by_id = {m.id: m for m in meters}
    result: list[Reading] = []
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

    if not meters_list:
        content = """
        <h1>Счётчики</h1>
        <p class="text-muted">Счётчиков пока нет.</p>
        """
        return HttpResponse(page("Счётчики", content))

    items = ""
    for meter in meters_list:
        items += (
            f'<li class="list-group-item">'
            f'<a href="/meters/{meter.id}/">'
            f"[{meter.id}] {meter.name}</a> ({meter.unit})"
            f"</li>"
        )

    content = f"""
    <h1>Счётчики</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Счётчики", content))


def meter_detail(request, meter_id):
    meters_list = _all_meters()
    meter = next((m for m in meters_list if m.id == meter_id), None)

    if meter is None:
        content = """
        <h1 class="text-danger">Счётчик не найден</h1>
        <a href="/meters/" class="btn btn-outline-secondary">
            ← к списку счётчиков
        </a>
        """
        return HttpResponse(
            page("Счётчик не найден", content), status=404
        )

    readings_list = _all_readings(meters_list)
    history = get_history(readings_list, meter_id)

    if history:
        history_items = "".join(
            f'<li class="list-group-item">{r}</li>' for r in history
        )
    else:
        history_items = (
            '<li class="list-group-item text-muted">'
            "Показаний нет</li>"
        )

    payment = create_payment(readings_list, meter_id)
    if payment is None:
        payment_info = "недостаточно данных"
    elif payment.amount is None:
        payment_info = "тариф не установлен"
    else:
        payment_info = f"{payment.amount:.2f} руб."

    tariff_str = (
        f"{meter.tariff:.2f} руб."
        if meter.tariff is not None
        else "не установлен"
    )

    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">{meter.name}</h5>
            <p class="card-text"><strong>ID:</strong> {meter.id}</p>
            <p class="card-text">
                <strong>Единица измерения:</strong> {meter.unit}
            </p>
            <p class="card-text">
                <strong>Тариф:</strong> {tariff_str}
            </p>
            <p class="card-text">
                <strong>Платёж:</strong> {payment_info}
            </p>
        </div>
    </div>

    <h3>История показаний</h3>
    <ul class="list-group">{history_items}</ul>

    <a href="/meters/" class="btn btn-outline-secondary mt-3">
        ← к списку счётчиков
    </a>
    """
    return HttpResponse(page(meter.name, content))

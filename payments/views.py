from django.http import HttpResponse

from homepage.views import page
from meters.views import _all_meters, _all_readings
from models.payments import create_payment


def payments(request):
    meters_list = _all_meters()
    readings_list = _all_readings(meters_list)

    items = ""
    for meter in meters_list:
        payment = create_payment(readings_list, meter.id)
        if payment is None:
            continue
        if payment.amount is None:
            amount_str = "тариф не установлен"
        else:
            amount_str = f"{payment.amount:.2f} руб."
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/payments/{meter.id}/">{meter.name}</a>'
            f"<span>{amount_str}</span>"
            f"</li>"
        )

    if not items:
        items = (
            '<li class="list-group-item text-muted">'
            "Платежей пока нет (нужно минимум два показания "
            "по счётчику)</li>"
        )

    content = f"""
    <h1>Платежи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Платежи", content))


def payment_detail(request, meter_id):
    meters_list = _all_meters()
    meter = next((m for m in meters_list if m.id == meter_id), None)

    if meter is None:
        content = """
        <h1 class="text-danger">Счётчик не найден</h1>
        <a href="/payments/" class="btn btn-outline-secondary">
            ← к списку платежей
        </a>
        """
        return HttpResponse(
            page("Счётчик не найден", content), status=404
        )

    readings_list = _all_readings(meters_list)
    payment = create_payment(readings_list, meter_id)

    if payment is None:
        content = f"""
        <h1 class="text-danger">Недостаточно данных</h1>
        <p>Для расчёта платежа по счётчику
        «{meter.name}» нужно минимум два показания.</p>
        <a href="/payments/" class="btn btn-outline-secondary">
            ← к списку платежей
        </a>
        """
        return HttpResponse(
            page("Недостаточно данных", content), status=200
        )

    consumption = (
        f"{payment.consumption:.2f} {meter.unit}"
        if payment.consumption is not None
        else "—"
    )
    tariff_str = (
        f"{payment.tariff:.2f} руб."
        if payment.tariff is not None
        else "не установлен"
    )
    amount_str = (
        f"{payment.amount:.2f} руб."
        if payment.amount is not None
        else "—"
    )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Платёж по счётчику «{meter.name}»
            </h5>
            <p class="card-text">
                <strong>Расход:</strong> {consumption}
            </p>
            <p class="card-text">
                <strong>Тариф:</strong> {tariff_str}
            </p>
            <p class="card-text">
                <strong>К оплате:</strong> {amount_str}
            </p>
            <a href="/payments/" class="btn btn-outline-secondary">
                ← к списку платежей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Платёж — {meter.name}", content))
from django.shortcuts import render
from meters.views import _all_meters, _all_readings
from models.payments import create_payment


def payments(request):
    meters_list = _all_meters()
    readings_list = _all_readings(meters_list)

    items = []
    for meter in meters_list:
        payment = create_payment(readings_list, meter.id)
        if payment is None:
            continue
        if payment.amount is None:
            amount_str = "тариф не установлен"
        else:
            amount_str = f"{payment.amount:.2f} руб."
        items.append({"meter": meter, "amount_str": amount_str})

    return render(request, "payments/payment_list.html", {"items": items})


def payment_detail(request, meter_id):
    meters_list = _all_meters()
    meter = next((m for m in meters_list if m.id == meter_id), None)
    if meter is None:
        return render(
            request,
            "payments/payment_detail.html",
            {"meter": None},
            status=404
        )

    readings_list = _all_readings(meters_list)
    payment = create_payment(readings_list, meter_id)

    context = {"meter": meter, "payment": payment}
    return render(request, "payments/payment_detail.html", context)

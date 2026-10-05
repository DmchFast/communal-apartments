from django.http import HttpResponse


def payments(request):
    return HttpResponse("Список платежей")


def payment_detail(request, meter_id):
    return HttpResponse(f"Платёж по счётчику {meter_id}")
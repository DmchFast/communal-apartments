from django.http import HttpResponse


def meters(request):
    return HttpResponse("Список счётчиков")


def meter_detail(request, meter_id):
    return HttpResponse(f"Счётчик {meter_id}")
from django.http import HttpResponse


def index(request):
    return HttpResponse("Коммунальные показания — сервис учёта")
from django.urls import path

from . import views

app_name = 'meters'

urlpatterns = [
    path("", views.meters, name="meters"),
    path("<int:meter_id>/", views.meter_detail, name="meter_detail"),
]

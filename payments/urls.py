from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path("", views.payments, name="payments"),
    path("stats/", views.statistics, name="statistics"),
    path("readings/", views.readings_by_period, name="readings_by_period"),
    path("<int:meter_id>/", views.payment_detail, name="payment_detail"),
]

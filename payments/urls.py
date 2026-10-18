from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path("", views.payments, name="payments"),
    path("stats/", views.statistics, name="statistics"),
    path("<int:meter_id>/", views.payment_detail, name="payment_detail"),
]

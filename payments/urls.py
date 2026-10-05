from django.urls import path

from . import views

urlpatterns = [
    path("", views.payments, name="payments"),
    path("<int:meter_id>/", views.payment_detail, name="payment_detail"),
]

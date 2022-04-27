from django.urls import path

from .views import OrdersView

urlpatterns = [
    path("", OrdersView.as_view({"get": "list"}), name="orders"),
    path("<int:order_id>/", OrdersView.as_view({"get": "retrieve"}), name="order_details"),
    path("<int:order_id>/complete/", OrdersView.as_view({"post": "complete_order"}), name="order_complete"),
    path("<int:order_id>/cancel/", OrdersView.as_view({"post": "cancel_order"}), name="order_cancel"),
]

from django.urls import path

from .views import ProductsView

urlpatterns = [
    path("", ProductsView.as_view({"get": "list"}), name="products"),
    path("<int:product_id>/", ProductsView.as_view({"get": "retrieve"}), name="product_details"),
    path("<int:product_id>/add-to-order/", ProductsView.as_view({"post": "add_to_order"}), name="product_add_to_order"),
    path(
        "<int:product_id>/remove-from-order/",
        ProductsView.as_view({"delete": "remove_from_order"}),
        name="product_remove_from_order",
    ),
]

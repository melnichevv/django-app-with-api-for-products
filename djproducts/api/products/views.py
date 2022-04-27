from django.db import transaction
from djproducts.apps.orders.services.order import add_product_to_order, get_or_create_order, remove_product_from_order
from djproducts.apps.products.models import Product
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import ProductSerializer


class ProductsView(ModelViewSet):
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"
    queryset = Product.objects.in_stock()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ("name", "price")
    ordering = ("name",)
    search_fields = ("name",)

    @transaction.atomic
    def add_to_order(self, request, *args, **kwargs):
        product = self.get_object()
        order = get_or_create_order(user=request.user)
        add_product_to_order(order=order, product=product)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def remove_from_order(self, request, *args, **kwargs):
        product = self.get_object()
        order = get_or_create_order(user=request.user)
        remove_product_from_order(order=order, product=product)
        return Response(status=status.HTTP_200_OK)

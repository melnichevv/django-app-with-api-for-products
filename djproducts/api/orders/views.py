from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from djproducts.apps.orders.models import Order
from djproducts.apps.orders.services.order import cancel_order, complete_order
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import OrderSerializer


class OrdersView(ModelViewSet):
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ("status",)
    ordering_fields = ("created_at", "status")
    ordering = ("-created_at",)

    def get_queryset(self):
        return (
            Order.objects.for_user(self.request.user)
            .annotate_total_price()
            .prefetch_related("order_products", "order_products__product")
        )

    @transaction.atomic
    def complete_order(self, request, *args, **kwargs):
        order = self.get_object()
        complete_order(order=order)
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def cancel_order(self, request, *args, **kwargs):
        order = self.get_object()
        cancel_order(order=order)
        return Response(status=status.HTTP_200_OK)

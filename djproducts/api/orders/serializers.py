from djproducts.api.core.serializers import BaseSerializer
from djproducts.api.products.serializers import ProductSerializer
from djproducts.apps.orders.models.order import OrderStatus
from rest_framework import serializers


class OrderProductSerializer(BaseSerializer):
    product = ProductSerializer(exclude=["quantity_in_stock", "created_at", "updated_at"])
    amount = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2, source="get_total_price")


class OrderSerializer(BaseSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    products = OrderProductSerializer(many=True, source="order_products", exclude=["created_at", "updated_at"])
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2, source="get_total_price")

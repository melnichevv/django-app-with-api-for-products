from djproducts.api.core.serializers import BaseSerializer
from rest_framework import serializers


class ProductSerializer(BaseSerializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    quantity_in_stock = serializers.IntegerField(source="current_quantity")

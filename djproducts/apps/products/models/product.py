from django.db import models
from django.db.models import Count, F, Q, query
from djproducts.apps.core.models.base import AbstractBaseModel
from djproducts.apps.orders.models.order import OrderStatus


class ProductQuerySet(query.QuerySet):
    def annotate_current_quantity(self):
        return self.annotate(
            in_progress_orders_amount=Count(
                "order_products__amount", filter=Q(order_products__order__status=OrderStatus.IN_PROGRESS)
            )
        ).annotate(current_quantity=F("quantity_in_stock") - F("in_progress_orders_amount"))

    def in_stock(self):
        return self.annotate_current_quantity().filter(current_quantity__gt=0)

    def out_of_stock(self):
        return self.annotate_current_quantity().filter(current_quantity__gt=0)


class ProductManager(models.Manager):
    def in_stock(self):
        return self.get_queryset().in_stock()

    def out_of_stock(self):
        return self.get_queryset().out_of_stock()


class Product(AbstractBaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    objects = ProductManager.from_queryset(ProductQuerySet)()

    def get_current_amount(self) -> int:
        from djproducts.apps.products.queries.product import get_current_amount

        return get_current_amount(self)

    @property
    def is_in_stock(self) -> bool:
        return self.get_current_amount() > 0

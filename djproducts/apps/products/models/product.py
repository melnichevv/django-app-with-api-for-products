from django.db import models
from django.db.models import query
from djproducts.apps.core.models.base import AbstractBaseModel


class ProductQuerySet(query.QuerySet):
    def in_stock(self):
        # TODO remove currently in progress orders
        return self.filter(quantity_in_stock__gt=0)

    def out_of_stock(self):
        # TODO remove currently in progress orders
        return self.filter(quantity_in_stock=0)


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

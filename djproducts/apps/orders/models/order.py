from django.db import models
from django.db.models import query
from django.utils.translation import gettext_lazy as _lazy
from djproducts.apps.core.models.base import AbstractBaseModel
from djproducts.apps.users.models import User


class OrderQuerySet(query.QuerySet):
    def in_progress(self):
        return self.filter(status=OrderStatus.IN_PROGRESS)

    def cancelled(self):
        return self.filter(status=OrderStatus.CANCELLED)

    def completed(self):
        return self.filter(status=OrderStatus.COMPLETED)

    def for_user(self, user: User):
        return self.filter(user=user)


class OrderManager(models.Manager):
    def in_progress(self):
        return self.get_queryset().in_progress()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def completed(self):
        return self.get_queryset().completed()

    def for_user(self):
        return self.get_queryset().for_user()


class OrderStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", _lazy("In progress")
    CANCELLED = "CANCELLED", _lazy("Cancelled")
    COMPLETED = "COMPLETED", _lazy("Completed")


class Order(AbstractBaseModel):
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS)
    user = models.ForeignKey("users.User", related_name="orders", on_delete=models.CASCADE)
    products = models.ManyToManyField("products.Product", through="orders.OrderProducts", related_name="orders")

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()


class OrderProductsQuerySet(query.QuerySet):
    def in_progress(self):
        return self.filter(order__status=OrderStatus.IN_PROGRESS)

    def cancelled(self):
        return self.filter(order__status=OrderStatus.CANCELLED)

    def completed(self):
        return self.filter(order__status=OrderStatus.COMPLETED)

    def for_user(self, user: User):
        return self.filter(order__user=user)


class OrderProductsManager(models.Manager):
    def in_progress(self):
        return self.get_queryset().in_progress()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def completed(self):
        return self.get_queryset().completed()

    def for_user(self):
        return self.get_queryset().for_user()


class OrderProducts(AbstractBaseModel):
    order = models.ForeignKey("orders.Order", related_name="order_products", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", related_name="order_products", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    objects = OrderProductsManager.from_queryset(OrderProductsQuerySet)()

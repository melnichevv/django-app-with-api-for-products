from django.db import transaction
from djproducts.apps.orders.models import Order
from djproducts.apps.orders.models.order import OrderProducts, OrderStatus
from djproducts.apps.products.exceptions import ProductOutOfStockException
from djproducts.apps.products.models import Product
from djproducts.apps.users.models import User


def get_or_create_order(user: User) -> Order:
    """
    Try to get order which is already in progress.

    If order wasn't found - create one.
    """
    order, _ = Order.objects.get_or_create(user=user, status=OrderStatus.IN_PROGRESS)
    return order


def cancel_order(order: Order) -> None:
    """Cancel order."""
    order.cancel()


@transaction.atomic
def complete_order(order: Order) -> None:
    """Complete order and decrease quantity_in_stock for each Product in Order."""
    order.complete()
    products = []
    for order_product in order.order_products.all():  # type: OrderProducts
        product: Product = order_product.product
        product.quantity_in_stock -= order_product.amount
        products.append(product)
    Product.objects.bulk_update(products, fields=["quantity_in_stock", "updated_at"])


def add_product_to_order(order: Order, product: Product) -> None:
    """Check product availability and if it's in stock add it to order or increase amount for already existing order."""
    if not product.is_in_stock:
        raise ProductOutOfStockException

    order_products, _ = OrderProducts.objects.get_or_create(order=order, product=product)
    order_products.amount += 1
    order_products.save(update_fields=["amount", "updated_at"])


def remove_product_from_order(order: Order, product: Product) -> None:
    """Remove one instance of product from order."""
    try:
        order_products = OrderProducts.objects.get(order=order, product=product)
    except OrderProducts.DoesNotExist:
        # this is expected so simply return
        return

    order_products.amount -= 1
    if order_products.amount == 0:
        order_products.delete()
    else:
        order_products.save(update_fields=["amount", "updated_at"])

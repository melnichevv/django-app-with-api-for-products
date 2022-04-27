from djproducts.apps.products.models import Product


def get_current_amount(product: Product) -> int:
    """Return current quantity in stock and subtract product amount in currently in progress orders."""
    return product.quantity_in_stock - sum(product.order_products.in_progress().values_list("amount", flat=True))

from django.conf import settings
from django.urls import include, path

from .utils.swagger import get_swagger_with_version

app_name = "api"

urlpatterns = [
    path("auth/", include("djproducts.api.auth.urls")),
    path("orders/", include("djproducts.api.orders.urls")),
    path("products/", include("djproducts.api.products.urls")),
    path("users/", include("djproducts.api.users.urls")),
]

if settings.DRF_YASG:
    schema_view = get_swagger_with_version(app_name)

    urlpatterns += [
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]

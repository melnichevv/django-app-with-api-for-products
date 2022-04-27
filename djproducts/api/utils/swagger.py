import os

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join("/api", schema.basePath[1:])
        return schema


def get_swagger_with_version(version):
    return get_schema_view(
        openapi.Info(
            title="Species Sequestration Tool API",
            default_version=version,
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        urlconf="djproducts.api.urls",
        generator_class=SchemaGenerator,
    )

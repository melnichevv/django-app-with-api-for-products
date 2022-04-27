# DRF
# https://www.django-rest-framework.org/tutorial/quickstart/
REST_FRAMEWORK = {
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "JSON_UNDERSCOREIZE": {"no_underscore_before_number": False},
    "DEFAULT_RENDERER_CLASSES": ("djproducts.api.utils.renderers.CustomJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.ScopedRateThrottle",),
    "EXCEPTION_HANDLER": "djproducts.api.utils.exception_handlers.exception_proxy_handler",
}

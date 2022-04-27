import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import exception_handler

from .renderers import CustomJSONRenderer

logger = logging.getLogger(__name__)


def exception_proxy_handler(exc, context):
    request = context.get("request")
    # Add custom renderer in case if accepted_renderer was not provided in the request and request processing was failed
    if not hasattr(request, "accepted_renderer"):
        request.accepted_renderer = CustomJSONRenderer
    if request and isinstance(request.accepted_renderer, TemplateHTMLRenderer):
        return exception_handler(exc, context)

    headers = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    log_level = logging.ERROR

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        exc.status_code = status_code = status.HTTP_401_UNAUTHORIZED
        log_level = logging.WARNING

    if isinstance(exc, ValidationError):
        status_code = exc.status_code
        log_level = logging.WARNING

    elif isinstance(exc, APIException):
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["X-Throttle-Wait-Seconds"] = f"{int(exc.wait)}"
        status_code = exc.status_code

    elif isinstance(exc, (Http404, ObjectDoesNotExist)):
        status_code = status.HTTP_404_NOT_FOUND

    elif isinstance(exc, (PermissionDenied, DjangoPermissionDenied)):
        status_code = status.HTTP_403_FORBIDDEN

    logger.log(log_level, exc, exc_info=True)

    return Response(data=exc, status=status_code, headers=headers)

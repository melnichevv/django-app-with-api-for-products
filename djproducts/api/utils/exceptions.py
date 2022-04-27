from django.utils.translation import gettext_lazy as _lazy
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseApiException(APIException):
    default_detail = _lazy("Something went wrong, please try again.")
    status_code = status.HTTP_400_BAD_REQUEST

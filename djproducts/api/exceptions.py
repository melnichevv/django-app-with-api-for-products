from django.utils.translation import gettext_lazy as _lazy
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseApiException(APIException):
    default_detail = _lazy("Something went wrong, please contact our support team.")
    status_code = status.HTTP_400_BAD_REQUEST


class ProductOutOfStockApiException(BaseApiException):
    default_detail = _lazy("Sorry. This product is out of stock.")
    status_code = status.HTTP_200_OK

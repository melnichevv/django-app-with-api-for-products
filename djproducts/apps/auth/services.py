from django.http import HttpResponse
from djproducts.apps.users.models import User
from djproducts.apps.users.services.user import user_record_login
from rest_framework_jwt.compat import set_cookie_with_token
from rest_framework_jwt.settings import api_settings


def jwt_login(*, response: HttpResponse, user: User) -> HttpResponse:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    if api_settings.JWT_AUTH_COOKIE:
        set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

    user_record_login(user=user)

    return response

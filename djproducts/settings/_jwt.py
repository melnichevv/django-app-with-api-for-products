import datetime

from env_utils import get_int

JWT_EXPIRATION_DELTA_DEFAULT = 60 * 60 * 24 * 30  # 30 days in seconds
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(
        seconds=get_int("DJANGO_JWT_EXPIRATION_DELTA", JWT_EXPIRATION_DELTA_DEFAULT)
    ),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_GET_USER_SECRET_KEY": lambda user: user.secret_key,
    "JWT_RESPONSE_PAYLOAD_HANDLER": "djproducts.api.users.utils.jwt_response_payload_handler",
    "JWT_AUTH_COOKIE": "jwt_token",
    "JWT_AUTH_COOKIE_SAMESITE": "None",
}

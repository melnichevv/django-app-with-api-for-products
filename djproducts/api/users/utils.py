from typing import Any

from djproducts.apps.users.models import User

from .serializers import JWTSerializer, MeSerializer


def user_get_me(*, user: User):
    return MeSerializer(user).data


def jwt_response_payload_handler(token, user: User = None, *args: Any, **kwargs: Any):
    return JWTSerializer({"token": token, "me": user}).data

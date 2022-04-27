from typing import Tuple

from django.core.management.utils import get_random_secret_key
from django.db import transaction
from django.utils import timezone

from ..models import User


def user_create(email, password=None, **extra_fields) -> User:
    """Create new User."""
    extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_record_login(*, user: User) -> User:
    """Record last login for User."""
    user.last_login = timezone.now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    """
    Change secret key for User.

    This invalidates JWT tokens.
    """
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True

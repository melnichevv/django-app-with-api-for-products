"""
Wrapped version of stdlib json.

This module always uses the DjangoModelJSONEncoder when dumping stuff,
so that we don't need to worry about Decimals, datetimes, times etc. causing things to blow up.

This is the json module you should be importing by default.
"""
from json import dumps as _dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


def dumps(obj, **kwargs):
    if "cls" not in kwargs:
        kwargs["cls"] = DjangoModelJSONEncoder
    return _dumps(obj, **kwargs)


class DjangoModelJSONEncoder(DjangoJSONEncoder):
    """Serialize Django model objects by calling `serialize` method."""

    def default(self, o):
        if isinstance(o, models.Model) and hasattr(o, "serialize"):
            return o.serialize()
        return super().default(o)


class JSONField(models.JSONField):
    """Subclass of JSONField updated to use ULIDAsStringJSONEncoder."""

    def __init__(self, *args, **kwargs):
        """Force use of the correct encoder."""
        kwargs["encoder"] = DjangoModelJSONEncoder
        super().__init__(*args, **kwargs)

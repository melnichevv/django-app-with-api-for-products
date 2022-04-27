import logging
import re
from functools import partial

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djproducts.apps.core.json import DjangoModelJSONEncoder
from rest_framework import exceptions, status
from rest_framework.renderers import JSONRenderer

from .codes import Code, Codes

logger = logging.getLogger(__name__)


re_camel_finder = re.compile(r"[a-z]_[a-z]")


def unpack_validation_message(packed_message):
    try:
        return packed_message.code, str(packed_message)
    except AttributeError:
        return None, packed_message


def underscore_to_camel(match):
    g = match.group()
    return g[0] + g[2].upper()


class CustomJSONRenderer(CamelCaseJSONRenderer):
    encoder_class = DjangoModelJSONEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = None
        if renderer_context and "response" in renderer_context:
            response = renderer_context["response"]

        data = self._transform_response(payload=data, response=response)

        return super().render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )

    def _transform_response(self, payload, response=None):
        meta = None

        if hasattr(response, "extra"):
            meta = response.extra.get("meta", None)

        if isinstance(payload, Exception):
            code, data = self._handle_exception(payload)

        elif isinstance(payload, Code):
            code, data = payload, payload.data
            if data is Code.unset:
                data = None
        else:
            data = payload
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                code = Codes.BAD_REQUEST
            elif response.status_code == status.HTTP_401_UNAUTHORIZED:
                code = Codes.AUTHENTICATION_ERROR
            else:
                code = Codes.OK

        resp = self._prepare_api_response(data, code, meta)
        return resp

    def _prepare_api_response(self, data, code, meta=None):
        resp = self._serialize_code(code, data=data)
        if meta is not None:
            resp["meta"] = meta
        return resp

    @staticmethod
    def _serialize_code(code, data=None, **extra):
        serializer_data = {
            "code": code.code_value,
            "status": code.code_name,
            "data": data,
        }
        if code.data is not Code.unset:
            serializer_data["data"] = code.data

        serializer_data["message"] = code.message if code.message is not Code.unset else None

        serializer_data.update(**extra)

        return serializer_data

    @staticmethod
    def _unpack_validation_error(validation_error, code=None):
        message_code, message = unpack_validation_message(validation_error)
        validation_code = Codes.validation_errors_map.get(message_code) or code

        if not validation_code:
            validation_code = Codes.validation_errors_map[Codes.ValidationAliases.DEFAULT]
        return validation_code, message

    @classmethod
    def _flatten_validation_errors(cls, errors, field_prefix=""):
        for field, msg in errors.items():
            if isinstance(msg, dict):
                for sub_field, sub_msg in cls._flatten_validation_errors(msg, field):
                    yield sub_field, sub_msg
            else:
                yield f"{field_prefix}.{field}" if field_prefix else field, msg

    def _handle_exception(self, exc):
        data = None

        if isinstance(
            exc,
            (exceptions.APIException, Http404, PermissionDenied, ObjectDoesNotExist),
        ):
            code = Codes.exceptions_map.get(exc.__class__.__name__, Codes.API_ERROR)

            if code.message is Code.unset:
                code = code(message=str(exc))

            if isinstance(exc, exceptions.ValidationError):
                data = exc.detail
                if code == Codes.API_ERROR:
                    code = Codes.VALIDATION_ERROR

                errors = []
                # form data as [(code, case, data), ... ]
                if hasattr(data, "items"):
                    for field, validation_errors in self._flatten_validation_errors(data):
                        field = re_camel_finder.sub(underscore_to_camel, field)

                        if not isinstance(validation_errors, (list, tuple)):
                            validation_errors = [validation_errors]

                        for validation_error in validation_errors:
                            validation_code, message = self._unpack_validation_error(validation_error)
                            errors.append(validation_code(message=message, data={"field": field}))
                    data = errors

                elif isinstance(data, (list, tuple)):
                    data = [c(message=m) for c, m in map(partial(self._unpack_validation_error, code=code), data)]

                elif data:
                    code = code(message=str(data))
                    data = None

                if data:
                    if len(data) > 1:
                        code = Codes.MULTIPLE_ERRORS
                        data = [self._serialize_code(code) for code in data]
                    else:
                        code, data = data[0], None
        else:
            code = Codes.INTERNAL_ERROR
        return code, data


class SimpleJSONRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        if not isinstance(data, (dict, list)):
            return b""
        return super().render(data, *args, **kwargs)

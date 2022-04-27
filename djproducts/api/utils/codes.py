from django.utils.translation import gettext_lazy as _lazy


class Code:
    unset = object()

    def __init__(self, code_value, code_name, message=unset, data=unset):
        """Setup code details."""
        self.code_value = code_value
        self.code_name = code_name
        self._message = message
        self.data = data

    def __call__(self, code_value=None, code_name=None, message=None, data=None):
        kwargs = {
            "code_value": code_value or self.code_value,
            "code_name": code_name or self.code_name,
            "message": message or self._message,
            "data": data or self.data,
        }
        return Code(**kwargs)

    @property
    def message(self):
        return str(self._message) if self._message is not self.unset else self._message

    def __str__(self):
        return _lazy(f"Codes: {self.code_name}")


class Codes:
    """Codes of all possible API responses."""

    OK = Code(0, _lazy("OK"))

    # Basic API errors
    ERROR = Code(1000, "Error", _lazy("Something went wrong."))
    INTERNAL_ERROR = Code(1001, "InternalError", _lazy("An internal error occurred."))
    API_ERROR = Code(1002, "BaseApiException", _lazy("Something went wrong."))

    # Common API errors
    PARSE_ERROR = Code(1100, "ParseError")
    BAD_REQUEST = Code(1101, "BadRequest")
    NOT_FOUND = Code(1102, "NotFound")
    METHOD_NOT_ALLOWED = Code(1103, "MethodNotAllowed")
    PERMISSION_DENIED = Code(1104, "PermissionDenied")

    # Authentication exceptions
    AUTHENTICATION_ERROR = Code(1200, "AuthenticationError")
    AUTHORIZATION_ERROR = Code(1201, "AuthorizationError")
    UNKNOWN_CREDENTIALS = Code(1202, "UnknownCredentials")
    EXPIRED_TOKEN_EXCEPTION = Code(1203, "ExpiredTokenException")

    # Validation errors
    VALIDATION_ERROR = Code(1300, "ValidationError")
    REQUIRED_VALUE = Code(1301, "RequiredValue")
    NON_NULLABLE_VALUE = Code(1302, "NonNullableValue")
    NON_BLANK_VALUE = Code(1303, "NonBlankValue")
    INVALID_VALUE = Code(1304, "InvalidValue")
    THROTTLED = Code(1305, "Throttled")

    # Multiple and complex exceptions
    MULTIPLE_ERRORS = Code(2000, "MultipleErrors", _lazy("Multiple errors happened."))

    class ValidationAliases:
        INVALID = "invalid"
        DEFAULT = "default"
        REQUIRED = "required"
        NULL = "null"
        BLANK = "blank"

    validation_errors_map = {
        ValidationAliases.DEFAULT: VALIDATION_ERROR,
        ValidationAliases.REQUIRED: REQUIRED_VALUE,
        ValidationAliases.NULL: NON_NULLABLE_VALUE,
        ValidationAliases.BLANK: NON_BLANK_VALUE,
        # Return generic ValidationError instead of specific InvalidValue because all validation errors get
        # invalid code by default, but in this case it'd be useful to remain them 'ValidationError's
        ValidationAliases.INVALID: VALIDATION_ERROR,
    }

    exceptions_map = {
        "Exception": INTERNAL_ERROR,
        "Http404": NOT_FOUND,
        "DoesNotExist": NOT_FOUND,
        "ObjectDoesNotExist": NOT_FOUND,
        "UserIsNotActive": AUTHORIZATION_ERROR,
        "NotAuthenticated": AUTHENTICATION_ERROR,
        "ExpiredTokenException": AUTHENTICATION_ERROR,
        "AuthenticationFailed": AUTHENTICATION_ERROR,
        "SocialAuthErrorApiException": AUTHENTICATION_ERROR,
    }

    for code in list(locals().values()):
        if isinstance(code, Code):
            exceptions_map[code.code_name] = code

    @classmethod
    def codes(cls):
        codes = {}
        for code_name, code in vars(cls).items():
            if isinstance(code, Code):
                codes[code_name] = (code.code_value, code.code_name)
        return codes

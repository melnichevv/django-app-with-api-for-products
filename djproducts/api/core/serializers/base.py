from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """
    A Base Serializer that takes an additional `only` argument that controls which fields should be displayed.

    Also this serializer provides fields, which are common for all models.
    """

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def __init__(self, *args, **kwargs):
        """Extend default __init__ method."""
        # Don't pass the "only" and "exclude" arguments up to the superclass
        only_fields = kwargs.pop("only", None)
        excluded_fields = kwargs.pop("exclude", None)

        if only_fields and excluded_fields:
            raise ValueError("'only' and 'exclude' fields are not allowed at the same time")

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if excluded_fields is not None:
            # Drop any fields that are specified in the "exclude" argument.
            existing = set(self.fields)
            excluded = set(excluded_fields)
            for field_name in excluded:
                if field_name in existing:
                    self.fields.pop(field_name)

        if only_fields is not None:
            # Drop any fields that are not specified in the "only" argument.
            allowed = set(only_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class EmptySerializer(serializers.Serializer):
    """Used in swagger when request body should be empty."""

from rest_framework import serializers


class UserInitSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, default="")
    last_name = serializers.CharField(required=False, default="")


class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class JWTSerializer(serializers.Serializer):
    token = serializers.CharField()
    me = MeSerializer()

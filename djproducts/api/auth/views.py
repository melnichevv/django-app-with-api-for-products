from django.conf import settings
from djproducts.apps.users.services.user import user_change_secret_key, user_record_login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView


class LoginView(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user") or request.user
        user_record_login(user=user)

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request):
        """Log out user by removing JWT cookie header and changing User's secret key."""
        user_change_secret_key(user=request.user)

        response = Response(status=status.HTTP_202_ACCEPTED)
        response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response

from djproducts.apps.users.queries.user import user_get_me
from rest_framework.response import Response
from rest_framework.views import APIView

from ..mixins import ApiAuthMixin, ApiErrorsMixin


class MeView(ApiAuthMixin, ApiErrorsMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(user_get_me(user=request.user))

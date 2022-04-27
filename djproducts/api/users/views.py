from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeSerializer


class MeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(MeSerializer(instance=request.user).data)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.cache import cache

from .seralizers import UserSerializer, SampleModelSerializer
from .rate_limiter import rate_limit
from . import models

User = get_user_model()

class SampleModelViewSet(ModelViewSet):
    queryset = models.SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    CACHE_KEY = "users_list_v1"
    CACHE_TTL = 300

    @rate_limit(max_requests=5, time_window=60)
    def list(self, request, *args, **kwargs):

        data = cache.get(self.CACHE_KEY)

        if data is None:
            print("🔥 DATABASE HIT")
            data = self.get_serializer(self.get_queryset(), many=True).data
            cache.set(self.CACHE_KEY, data, self.CACHE_TTL)
        else:
            print("⚡ CACHE HIT")

        return Response(data)

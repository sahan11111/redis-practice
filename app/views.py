
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.cache import cache
import redis
import json
from .seralizers import UserSerializer, SampleModelSerializer
from .rate_limiter import rate_limit
from . import models

r=redis.Redis(host='localhost', port=6379, db=0)
User = get_user_model()

class SampleModelViewSet(ModelViewSet):
    queryset = models.SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

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


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        message = {
            "event": "USER_CREATED",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }

        r.publish("user_notifications", json.dumps(message))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
        
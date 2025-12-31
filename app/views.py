from urllib import response
from . import seralizers
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.response import Response

User=get_user_model()



class SampleModelViewSet(ModelViewSet):
    queryset = seralizers.models.SampleModel.objects.all()
    serializer_class = seralizers.SampleModelSerializer
  
    
class UserViewSet(ModelViewSet):
    queryset = seralizers.get_user_model().objects.all()
    serializer_class = seralizers.UserSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        cache_key = "users-data"
        data = cache.get(cache_key)

        if data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 300)

        return Response(data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = seralizers.UserSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = "users_list_v1"
        data = cache.get(cache_key)

        if data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=300)  # 5 minutes

        return Response(data)
    
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = seralizers.UserSerializer
#     permission_classes = [AllowAny]

#     CACHE_KEY = "users_list_v1"
#     CACHE_TTL = 100  

#     def list(self, request, *args, **kwargs):
#         data = cache.get(self.CACHE_KEY)

#         if data is None:
#             print("🔥 DATABASE HIT")
#             serializer = self.get_serializer(self.get_queryset(), many=True)
#             data = serializer.data
#             cache.set(self.CACHE_KEY, data, self.CACHE_TTL)
#         else:
#             print("⚡ CACHE HIT")

#         return Response(data)


        
    
    
    
    
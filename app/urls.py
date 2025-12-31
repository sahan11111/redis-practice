from django.urls import path
from . import views

urlpatterns = [
    path('sample/', views.SampleModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='sample-model'),
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
]
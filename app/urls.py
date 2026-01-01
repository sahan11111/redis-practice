from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'users',views.UserViewSet,basename='user')

urlpatterns = [
    path('sample/', views.SampleModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='sample-model'),
    path('', include(router.urls)),
]
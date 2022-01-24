from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Import ViewSet
from .api import UserViewSet

router = DefaultRouter()

router.register('user', UserViewSet, basename='users')

# url to login user
urlpatterns = [
    path('login/', obtain_auth_token, name='login')
]

urlpatterns += router.urls

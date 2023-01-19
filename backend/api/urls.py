from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import create_token, create_user, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include([
        path('token/login/', create_token),
        path('signup/', create_user)
    ]))
]
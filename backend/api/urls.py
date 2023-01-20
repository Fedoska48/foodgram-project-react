from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import create_token, create_user, UserViewSet, TagViewSet, \
    RecipeViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()

# user
router.register(r'users', UserViewSet, basename='users')
# subscribe
router.register(r'users/(?P<user_id>\d+)/subscribe/', TagViewSet,
                basename='tags')
# tag
router.register(r'tags', TagViewSet, basename='tags')
# recipe
router.register(r'recipes', RecipeViewSet, basename='recipes')
# ingredient
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
# shopping_cart
router.register(r'recipes/download_shopping_cart/', TagViewSet,
                basename='tags')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart/', TagViewSet,
                basename='tags')
# favorite
router.register(r'recipes/(?P<recipe_id>\d+)/favorite/', TagViewSet,
                basename='tags')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', include([
        path('login/', create_token),
        path('logout/', delete_token)
    ]))
]

from datetime import datetime

from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action

from .filters import RecipeFilter, IngredientFilter
from .pagination import StandartPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          ShoppingCartSerializer, FavoriteSerializer,
                          SubscribeSerializer, SubscriptionSerializer,
                          RecipeShortSerializer, RecipeReadSerializer,
                          RecipeCreateUpdateSerializer, UserReadSerializer,
                          UserCreateSerializer)
from recipes.models import (Recipe, Tag, Ingredient, Subscribe, Favorite,
                            ShoppingCart, IngredientInRecipe)
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    """Кастомный вьюсет рецептов модели Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filterset_class = RecipeFilter
    pagination_class = StandartPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        if self.action in ('shopping_cart', 'favorite'):
            return RecipeShortSerializer
        return RecipeCreateUpdateSerializer

    @staticmethod
    def export_file(ingredients):
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["name"]}, '
                f'{ingredient["amount"]} '
                f'{ingredient["measurement_unit"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        date = datetime.today()
        filename = f'{date}_shopping_list.txt'
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        user = request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=user).values(
            name=F('ingredients__name'),
            measurement_unit=F('ingredients__measurement_unit')).annotate(
            amount=Sum('amount').order_by('ingredients__name')
        )
        return self.export_file(ingredients)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        """Список покупок."""
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            data = {
                'user': user.pk,
                'recipe': recipe.pk
            }
            serializer = ShoppingCartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            message = {
                'detail':
                    'Рецепт удален из корзины'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def favorite(self, request, pk):
        """Функционал избранных рецептов."""
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            data = {
                'user': user.pk,
                'recipe': recipe.pk
            }
            serializer = FavoriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, pk=pk)
            Favorite.objects.filter(user=user, recipe=recipe).delete()
            message = {
                'detail':
                    'Рецепт удален из избранного'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Стандартный ридонли вьюсет тегов модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Стандартный ридонли вьюсет ингридиентов модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)
    permission_classes = [AllowAny, ]


class FoodgramUserViewSet(UserViewSet):
    """Кастомный ViewSet модели User."""
    queryset = User.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = StandartPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserReadSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action in ('subscriptions', 'subscribe'):
            return SubscriptionSerializer
        return UserCreateSerializer  # есть аналогичный из djoser

    @action(
        detail=False,
        methods=['GET', ],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def subscriptions(self, request):
        """Список подписок."""
        user = request.user
        subscriptions = User.objects.filter(
            following__user=user
        )
        page = self.paginate_queryset(subscriptions)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def subscribe(self, request, id):
        """Функционал подписок на авторов."""
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            user = request.user
            author = get_object_or_404(User, pk=id)
            data = {
                'user': user.pk,
                'author': author.pk
            }
            serializer = SubscribeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user = request.user
            Subscribe.objects.get_object_or_404(
                user=user, author=author
            ).delete()
            message = {
                'detail': f'Вы отписались от пользователя {author}'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)

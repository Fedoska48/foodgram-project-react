from datetime import datetime
from smtplib import SMTPResponseException

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets, request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import TagSerializer, \
    IngredientSerializer, \
    ShoppingCartSerializer, FavoriteRecipeSerializer, \
    SubscribeSerializer
from recipes.models import Recipe, Tag, Ingredient, \
    Subscribe, FavoriteRecipe, ShoppingCart, IngredientInRecipe
from users.models import User
from .permissions import IsAdminUser
from .serializers import IngredientInRecipeSerializer, RecipeReadSerializer, \
    RecipeCreateUpdateSerializer, UserReadSerializer, UserCreateSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Кастомный вьюсет рецептов модели Recipe."""
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateUpdateSerializer
        # return RecipeReadSerializer

    @action(detail=False, methods=['GET', ])
    def download_shopping_cart(self, request):
        shopping_cart = IngredientInRecipe.objects.filter(
            recipe__shoppingcart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total_amount=Sum('amount'))
        text = [(f'Список покупок:\n',
                 f'Ингридиент:{ingridient["ingredient__name"]};\n'
                 f'Ингридиент:{ingridient["ingredient__measurement_unit"]};\n'
                 f'Ингридиент:{ingridient["amount"]}.\n')
                for ingridient in shopping_cart
                ]
        date = datetime.today()
        filename = f'{date}_shopping_list.txt'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        # permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe__id=pk).exists():
                return Response({'errors': 'Рецепт уже в списке покупок'},
                                status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = ShoppingCart.object.create(user=request.user,
                                                       recipe=recipe)
            serializer = ShoppingCartSerializer(data=shopping_cart)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shopping_cart = get_object_or_404(ShoppingCart, user=request.user,
                                              recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        # permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if FavoriteRecipe.objects.all(user=request.user,
                                          recipe__id=pk).exists():
                return Response({'errors': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            favorite = FavoriteRecipe.object.create(user=request.user,
                                                    recipe=recipe)
            serializer = FavoriteRecipeSerializer(data=favorite)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(FavoriteRecipe, user=request.user,
                                         recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Стандартный ридонли вьюсет тегов модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Стандартный ридонли вьюсет ингридиентов модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FoodgramUserViewSet(UserViewSet):
    """Кастомный ViewSet модели User."""
    queryset = User.objects.all()

    # permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'get':
            return UserReadSerializer
        return UserCreateSerializer  # есть аналогичный из djoser

    @action(
        detail=False,
        methods=['GET', ],
        # permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            following__user=request.user).select_related('author')
        serializer = SubscribeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        # permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if request.user == author:
                return Response({'errors': 'Попытка подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            data = Subscribe.objects.get_or_create(user=request.user,
                                                   author=author)
            serializer = FavoriteRecipeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = Subscribe.objects.get_object_or_404(user=request.user,
                                                       author=author)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

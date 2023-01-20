from smtplib import SMTPResponseException

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from backend.api.serializers import RecipeSerializer, TagSerializer, \
    IngredientSerializer, CreateTokenSerializer, CreateUserSerializer, \
    UserSerializer, ShoppingCartSerializer, FavoriteRecipeSerializer, \
    SubscribeSerializer
from backend.backend import settings
from backend.recipes.models import Recipe, Tag, Ingredient, \
    Subscribe, FavoriteRecipe, ShoppingCart
from backend.users.models import User
from .permissions import IsAdminUser


class RecipeViewSet(viewsets.ModelViewSet):
    """Полный цикл CRUD"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """GET-списка тегов и GET-конкретного тега"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """GET-list, GET-detail"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    """Мои подписки GET, подписаться POST и отписаться DEL"""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    """POST добавл. рецепта в избранное и DEL удал. рецепта в избранное"""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Скачать список покупок (GET), добавить (POST) и удалить рецепт (DEL)"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели User."""
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(
        detail=False,
        methods=(['GET', 'PATCH']),
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Текущий пользователь."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)

    @action(
        methods=(['PATCH']),
        permission_classes=[IsAuthenticated],
    )
    def set_password(self, request):
        """Изменение пароля."""
        pass

    @action(
        detail=False,
        methods=(['GET']),
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        """Мои подписки."""
        pass


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """Создание нового пользователя."""
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    token = default_token_generator.make_token(user)

    try:
        send_mail(
            'confirmation code',
            token,
            settings.MAILING_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except SMTPResponseException:
        user.delete()
        return Response(
            data={'error': 'Ошибка при отправки кода подтверждения!'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    """Создание JWT-токена для пользователей."""
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')
    token = default_token_generator.check_token(user, confirmation_code)

    if token == serializer.validated_data.get('confirmation_code'):
        jwt_token = RefreshToken.for_user(user)
        return Response(
            {'token': f'{jwt_token}'}, status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Отказано в доступе'},
        status=status.HTTP_400_BAD_REQUEST
    )

from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, Subscribe, \
    FavoriteRecipe, ShoppingCart
from rest_framework.relations import StringRelatedField
from users.models import User


# TAGS ZONE
from recipes.models import IngredientInRecipe


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# INGREDIENTS ZONE
class IngredientSerializer(serializers.ModelSerializer):
    """Ingredients serializer."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class UserReadSerializer(serializers.ModelSerializer):
    """User for GET method."""

    class Meta:
        model = User
        fields = (
        'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


class UserCreateSerializer(serializers.ModelSerializer):
    """User for POST method in create user action."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Ingredients in Recipe serializer."""
    recipe = serializers.StringRelatedField(many=True, read_only=True)
    ingredients = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'recipe', 'ingredients', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserReadSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',  # link
            'author',  # link
            'ingredients',  # link
            'is_favorited',  # method
            'is_in_shopping_cart',  # method
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        queryset = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(queryset, many=True)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=request.user,
                                             recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe=obj).exists()

# PRODUCTION LINE --------------------------------------------PROD ^

class SubscribeSerializer(serializers.ModelSerializer):
    """Subscribe serializer."""

    class Meta:
        model = Subscribe
        fields = ('user', 'author')


class FavoriteRecipeSerializer(serializers.Serializer):
    """Favorite Recipe serializer."""

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.Serializer):
    """ShoppingCart serializer."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'ingredients')


# RECIPE ZONE
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=request.user,
                                             recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe=obj).exists()


# USERS ZONE
class FoodgramUserSerializer(serializers.ModelSerializer):
    """Serializer модели User."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer создания нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено!"
            )
        return data


class CreateTokenSerializer(serializers.ModelSerializer):
    """Serializer создания JWT-токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)

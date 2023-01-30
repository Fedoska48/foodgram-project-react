from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from djoser import serializers as ds
from recipes.models import (Recipe, Tag, Ingredient, Subscribe, Favorite,
                            ShoppingCart)
from djoser.serializers import (UserCreateSerializer, UserSerializer,
                                SetPasswordSerializer)
from rest_framework.fields import SerializerMethodField
from users.models import User

from recipes.models import IngredientInRecipe


# USERS ZONE
class UserReadSerializer(UserSerializer):
    """USER for READ: GET: api/users/ :: /api/users/{id}/ :: /api/users/me/."""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta(ds.UserSerializer.Meta):
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, user):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return (
                request.user.is_authenticated
                and user.follower.filter(user=request.user).exists()
        )


class UserCreateSerializer(UserCreateSerializer):
    """Функционал регистрации пользователя: POST: api/users/"""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SetPasswordSerializer(SetPasswordSerializer):
    """Смена пароля. POST: api/users/set_password/."""

    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписки. POST, DEL: /api/users/{id}/subscribe/"""

    class Meta:
        model = Subscribe
        fields = ('user', 'author')

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                {
                    'error': 'Ошибка подписки. Попытка подписаться на себя.'
                }
            )
        return data


class SubscriptionSerializer(UserReadSerializer):
    """Сериализатор списка подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()[:(int(recipes_limit))]
        else:
            recipes = obj.recipes.all()
        return RecipeShortSerializer(recipes, many=True).data


# TAGS ZONE
class TagSerializer(serializers.ModelSerializer):
    """Сериализато тегов. GET: api/tags/ :: api/tags/{id}/"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# INGREDIENTS ZONE
class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты. GET: api/ingredients/ :: api/ingredients/{id}/"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Ингредиенты в рецепте. Include in RecipeReadSerializer. OK"""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


# RECIPES ZONE
class RecipeReadSerializer(serializers.ModelSerializer):
    """Чтение рецептов. GET: api/recipes/ :: api/recipes/{id}/"""
    tags = TagSerializer(many=True, read_only=True)
    author = UserReadSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',  # link
            'author',  # link
            'ingredients',  # method
            'is_favorited',  # method
            'is_in_shopping_cart',  # method
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        """Custom queryset: filter IngredientInRecipe by recipe."""
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe_ingredients__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe=obj).exists()


class IngredientInRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Ингредиенты в рецепте доп. Include RecipeCreateUpdateSerializer"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание и обновление рецепта. POST: api/recipes/"""
    ingredients = IngredientInRecipeCreateUpdateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create_ingredients(self, ingredients, recipe):
        """Создать ингредиент."""
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredients=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, data):
        """Создать рецепт."""
        request = self.context.get('request')
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, data):
        """Обновить рецепт."""
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        instance = super().update(instance, data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(recipe=instance, ingredients=ingredients)
        instance.save()
        return self.instance


class RecipeShortSerializer(RecipeReadSerializer):
    """Короткая версия рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(RecipeShortSerializer):
    """Список покупок. POST/DELETE: api/recipes/{id}/shopping_cart/"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class FavoriteSerializer(RecipeShortSerializer):
    """Сериализатор избранного."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

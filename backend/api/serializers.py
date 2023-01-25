from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, Subscribe, \
    FavoriteRecipe, ShoppingCart
from rest_framework.relations import StringRelatedField
from users.models import User


from recipes.models import IngredientInRecipe


# USERS ZONE

class UserReadSerializer(serializers.ModelSerializer):
    """USER for READ: GET: api/users/ :: /api/users/{id}/ :: /api/users/me/."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """For USER registration: POST: api/users/"""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

# под вопросом что делать с "Изменение пароля", "Получить токен", "Удаление токена"

# TAGS ZONE
class TagSerializer(serializers.ModelSerializer):
    """Tags serializer. GET: api/tags/ :: api/tags/{id}/"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# INGREDIENTS ZONE
class IngredientSerializer(serializers.ModelSerializer):
    """Ingredients READ. GET: api/ingredients/ :: api/ingredients/{id}/"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Ingredients in Recipe serializer. Include in RecipeReadSerializer. OK"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


# RECIPES ZONE
class RecipeReadSerializer(serializers.ModelSerializer):
    """For READ Recipes. GET: api/recipes/ :: api/recipes/{id}/"""
    tags = TagSerializer(many=True, read_only=True)
    author = UserReadSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

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


class IngredientInRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Exists ingredient. New amount. Include RecipeCreateUpdateSerializer"""
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """"For CU Recipes. POST: api/recipes/"""
    ingredients = IngredientInRecipeCreateUpdateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(read_only=True)  # точно read_ony?

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

# для delete recipe надо что-то?

class ShoppingCartSerializer(serializers.Serializer):
    """ShoppingCart serializer. POST/DELETE: api/recipes/{id}/shopping_cart/"""
    # дописать

    class Meta:
        model = ShoppingCart
        fields = ('user', 'ingredients')

    def to_representation(self, value):
        # ('id', 'name', 'image', 'cooking_time')
        pass

    def to_internal_value(self, data):
        # ('id', 'name', 'image', 'cooking_time')
        pass


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    # дописать
    class Meta:
        model = Recipe
        # ('id', 'name', 'image', 'cooking_time')
        fields = ('user', 'recipe')




class SubscribeSerializer(serializers.ModelSerializer):
    """Subscribe serializer."""
    # дописать
    class Meta:
        model = Subscribe
        fields = ('user', 'author')

    def to_representation(self, instance):
        pass


class FavoriteRecipeSerializer(serializers.Serializer):
    """Favorite Recipe serializer."""
    # дописать
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        pass

# PRODUCTION LINE --------------------------------------------PROD ^

# class CreateTokenSerializer(serializers.ModelSerializer):
#     """Serializer создания JWT-токена для пользователей."""
#     username = serializers.CharField()
#     confirmation_code = serializers.CharField()
#
#     class Meta:
#         model = User
#         fields = ('username', 'confirmation_code',)

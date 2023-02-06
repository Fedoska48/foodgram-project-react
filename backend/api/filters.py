import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    """Кастомный фильтр."""
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=Recipe.objects.all(),
        field_name='author__id',
        to_field_name='id',
    )
    is_favorited = django_filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(
                recipes_favorite_related__user=user,
            )
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(
                recipes_shoppingcart_related__user=user,
            )
        return Recipe.objects.all()


class IngredientFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)

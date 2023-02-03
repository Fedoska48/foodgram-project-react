from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Recipe, Tag, Ingredient, IngredientInRecipe, Favorite


class IngredientInRecipeInLine(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1
    min_num = 1
    autocomplete_fields = ('ingredients',)


class RecipeAdmin(admin.ModelAdmin):

    def favorited_count(self):
        return Favorite.objects.filter(recipe=self.id).count()

    def ingredient_in_recipe(self):
        return ", ".join(map(str, self.recipe_ingredients.all()))

    list_display = (
        'id',
        'author',
        'name',
        'pub_date',
        'update',
        favorited_count,
        ingredient_in_recipe
    )
    list_display_links = (
        'author',
        'name',
    )
    search_fields = (
        'name',
        'text',
        'tags',
        'author',
        'tags'
    )

    # raw_id_fields = ('author', 'tags')
    inlines = (IngredientInRecipeInLine,)
    empty_value_display = '-пусто-'
    readonly_fields = ('pub_date', 'update')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.unregister(Group)

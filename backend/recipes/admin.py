from django.contrib import admin

from .models import Recipe, Tag, Ingredient, IngredientInRecipe


class IngredientInRecipeInLine(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1
    fields = ('ingredients', 'amount')
    autocomplete_fields = ('ingredients',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'pub_date',
        'update'
    )
    list_display_links = (
        'author',
        'name',
        'text',
    )
    search_fields = (
        'name',
        'text',
        'tags',
        'author',
        'tags'
    )

    raw_id_fields = ('author', 'tags')
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

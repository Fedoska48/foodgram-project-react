from django.contrib import admin

from .models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    # последовательность имен полей для вывода в списке записей
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    # поля, которые должны вести на страницу правки
    list_display_links = (
        'name',
        'text'
    )
    # поля по которых должна выполняться фильтация
    search_fields = (
        'author',
        'name',
        'text'
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name',)


# регистрация моделей в панели администратора
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)

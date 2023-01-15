from django.contrib import admin

from .models import Recipe, Tag, Ingredients, Product, Measure


class RecipeAdmin(admin.ModelAdmin):
    # последовательность имен полей для вывода в списке записей
    list_display = (
        'id',
        'author',
        'title',
        'image',
        'text',
        'duration'
    )
    # поля, которые должны вести на страницу правки
    list_display_links = (
        'title',
        'text'
    )
    # поля по которых должна выполняться фильтация
    search_fields = (
        'author',
        'title',
        'text'
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'slug')
    list_display_links = ('title', 'slug')
    search_fields = ('title', 'slug')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'measure')
    list_display_links = ('title', 'amount')
    search_fields = ('title', 'amount')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)


# регистрация моделей в панели администратора
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Measure, MeasureAdmin)

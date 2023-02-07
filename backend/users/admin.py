from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):

    def subscriptions_count(self, user):
        return user.following.count()

    def recipes_count(self, user):
        return user.recipes.count()

    subscriptions_count.short_description = 'Подписок'
    recipes_count.short_description = 'Рецептов'

    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'bio',
        'subscriptions_count',
        'recipes_count'
    )
    list_display_links = (
        'id',
    )
    search_fields = (
        'username',
    )


admin.site.register(User, UserAdmin)

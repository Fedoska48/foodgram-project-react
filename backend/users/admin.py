from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'bio',
    )
    list_display_links = (
        'id',
    )
    search_fields = (
        'username',
    )


admin.site.register(User, UserAdmin)

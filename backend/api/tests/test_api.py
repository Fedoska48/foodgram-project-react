from django.urls import reverse
from rest_framework.test import APITestCase

from backend.recipes.models import Recipe


class RecipesTestCase(APITestCase):
    def test_get(self):
        recipe_1 = Recipe.objects.create(
            author = 'Vasya',
            name = 'Shashlyk',
            text = 'Shashlyk iz myasa',

        )
        url = reverse('recipe-list')
        response = self.client.get(url)
        print(response.data)
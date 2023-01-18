from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=155
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/recipes',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    # is_favorited = models.BooleanField(default=False)
    # is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=55
    )
    color = models.CharField(
        verbose_name='HEX-код',
        max_length=11
    )
    slug = models.SlugField(
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
    )
    measurement_unit = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique measurement_unit')]


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_recipe',
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique ingredient')]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name="Подписчик"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Автор"
    )

class Product(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Measure(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=155,
        unique=True
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'




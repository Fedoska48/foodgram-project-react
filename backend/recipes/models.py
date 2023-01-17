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
        'Название',
        max_length=155
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/image/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField('Ingredient') # уточнение
    tags = models.ManyToManyField('Tag') # связь с моделью тегов
    cooking_time = models.IntegerField('Время приготовления')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    name = models.CharField('Тег', max_length=155)
    color = models.CharField('HEX-код', max_length=155)
    slug = models.SlugField('Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT,
        # related_name='name'
    )
    amount = models.FloatField('Количество')
    measurement_unit = models.ForeignKey(
        'Measure',
        on_delete=models.PROTECT,
        # related_name='name'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Product(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Measure(models.Model):
    name = models.CharField('Название', max_length=155, unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

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


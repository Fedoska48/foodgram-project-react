from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
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
    ingredients = models.ManyToManyField('Ingredients') # уточнение
    tags = models.ManyToManyField('Tag') # связь с моделью тегов
    duration = models.IntegerField('Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class Tag(models.Model):
    title = models.CharField('Тег', max_length=155)
    color = models.CharField('HEX-код', max_length=155)
    slug = models.SlugField('Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Ingredients(models.Model):
    title = models.ForeignKey('Product', on_delete=models.PROTECT)
    amount = models.FloatField('Количество')
    measure = models.ForeignKey('Measure', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Product(models.Model):
    title = models.CharField('Название', max_length=155, unique=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Measure(models.Model):
    title = models.CharField('Название', max_length=155, unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


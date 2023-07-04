from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        'Название категории',
        max_length=100)
    slug = models.SlugField(
        'Читабельный url категории',
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        'Название жанра',
        max_length=100)
    slug = models.SlugField(
        'Читабельный url жанра',
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=200)
    year = models.IntegerField(
        'Год создания',
        blank=True,
        validators=[MaxValueValidator(int(datetime.now().year))],)
    description = models.TextField(
        'Описание',
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name

from datetime import datetime

from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.core.validators import (
    MinValueValidator, MaxValueValidator, validate_email)
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, ADMIN.title()),
        (MODERATOR, MODERATOR.title()),
        (USER, USER.title()),
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        validators=[validate_email],
        help_text='Введите адрес электронной почты',
        error_messages={
            'unique': "Пользователь с данным email уже существует.",
        }
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text='Введите имя пользователя',
        error_messages={
            'unique': "Пользователь с указанным username уже существует.",
        },
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER,
        help_text='Роль пользователя'
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        help_text='Биография пользователя'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]


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
        blank=True,
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
    

class GenreTitle(models.Model):
    """Служебная модель для БД."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель отзыва."""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        help_text='Укажите рейтинг от 1 до 10',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст отзыва",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата размещения отзыва",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            ),
        ]
        ordering = ("-pub_date",)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    """Модель комментария к отзыву."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата размещения комментария",
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст комментария",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

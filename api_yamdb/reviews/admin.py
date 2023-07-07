from django.contrib import admin

from .models import Category, Genre, Title, User, Review, Comment


admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    list_editable = ('name', 'year', 'description')
    search_fields = ('name', 'year', 'category', 'genre')
    list_filter = ('name', 'year', 'category', 'genre')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'pub_date')
    search_fields = ('author', 'title', 'text', 'score')
    list_filter = ('author', 'title', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'pub_date')
    search_fields = ('author', 'review', 'text')
    list_filter = ('author', 'review', 'pub_date')
    list_editable = ('text',)

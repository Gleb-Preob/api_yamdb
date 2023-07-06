from django.contrib import admin

from .models import Category, Genre, Title, User


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

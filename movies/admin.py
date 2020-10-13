from django.contrib import admin
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'url')  # Конфигурирует список наших записей
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Класс, что мы видели отзывы которые прикреплены к данному фильму"""
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    """Класс, что б мы видели какие кадры из фильмы прикрепленны к фильму"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')  # Фильтрация и по какому полю филтровать
    search_fields = ('title', 'category__name')  # Поиск
    inlines = [MovieShotsInline, ReviewInline]
    form = MovieAdminForm
    save_on_top = True  # Кнопку сохранить перенети наверх
    save_as = True  # Появляется кнопка "сохранить как новый объект"
    list_editable = ('draft',)  # Как чекбокс в html, позволяет ставить галки в дисплее
    # fieldsets Группировать поля в одну строку
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actor', {
            'classes': ('collapse',),
            'fields': (('directors', 'actors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Option', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="50"')

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')  # Запретить редактирование


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Режиссеры и Актеры"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50"')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src{obj.image.url} width="50" height="50">')

    get_image.short_description = 'Изображение'  # Как будет называться наш стобец в админки


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Звезды рейтинга"""
    list_display = ('value',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('ip', 'movie', 'star')


admin.site.site_title = 'Администрация проекта'
admin.site.site_header = 'Администрация проекта'  # Поменять "администриование Django" на что нибудь получше

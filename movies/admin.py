from django.contrib import admin
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews


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


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')  # Фильтрация и по какому полю филтровать
    search_fields = ('title', 'category__name')  # Поиск
    inlines = [ReviewInline]
    save_on_top = True  # Кнопку сохранить перенети наверх
    save_as = True  # Появляется кнопка "сохранить как новый объект"
    list_editable = ('draft',)  # Как чекбокс в html, позволяет ставить галки в дисплее
    # fieldsets Группировать поля в одну строку
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', 'poster')
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


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')  # Запретить редактирование


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Режиссеры и Актеры"""
    list_display = ('name', 'age', 'image')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Звезды рейтинга"""
    list_display = ('value', )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('ip', 'movie', 'star')

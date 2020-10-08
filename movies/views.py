from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie


class MoviesView(ListView):
    """Список фильмок"""

    model = Movie  # Модель с которой будем работать
    queryset = Movie.objects.filter(draft=False)
    # ORM запрос к БД, фильтровать по полю draft, значение False, т.е где фильмы не черновик
    template_name = 'movies/movie_list.html'  # Шаблон


class MovieDetailView(DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = 'url'

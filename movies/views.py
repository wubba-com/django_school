from django.shortcuts import render
from django.views.generic.base import View
from .models import Movie


class MoviesView(View):
    """Список фильмок"""

    def get(self, request): # request - вся инфа присланная от клиента (браузера)
        movies = Movie.objects.all()
        return render(request, 'movies/movies_list.html', {'movies_list': movies})

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie
from .forms import ReviewForm


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


class AddReview(View):
    """Отправка отзыва"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)  # Импортировали форму и создали объект формы.
        # Затем используя форму и передавая в нее request.POST таким образом
        # джанго заполнит нашу форму данными, которые пришли к нам из запроса
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False, значит что мы хотим приостановить
            # сохранение нашей формы. Теперь мы можем внести изменеие в нашу форму
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

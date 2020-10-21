from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm
from django.db.models import Q


class GenreYear:
    """Реализация фильтров жанров и годов нашего фильтра"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """Список фильмок"""

    model = Movie  # Модель с которой будем работать
    queryset = Movie.objects.filter(draft=False)
    # ORM запрос к БД, фильтровать по полю draft, значение False, т.е где фильмы не черновик
    template_name = 'movies/movie_list.html'  # Шаблон

    def get_context_data(self, *args, **kwargs):
        """Вывод всех категории (напрмиер, в навигации)"""
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = 'url'  # атрибут отвечает за то, по какому полю нужно будет искать нашу запись

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm
        return context


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


class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'  # Поле по которому мы будем искать наших актеров


class FilterMovieView(ListView):
    """Создание фильтра фильма"""

    def get_queryset(self):
        """Будем фильтровать наши фильмы, там где года будут
        входить в список, который будет нам возвращаться с
        front-end, это список наших годов"""
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) | Q(genres__in=self.request.GET.getlist('genre'))
            # getlist('genre') - 'genre' name из формы
        )
        # | - логичкская ИЛИ
        return queryset


class AddStarRating(View):
    """Добавление рейтинга к фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return redirect('/')
        else:
            return HttpResponse(status=400)

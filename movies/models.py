from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категории', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    # SlugField - Текстовое поле содержащие
    # только буквы цифры, подчеркивания и дефисы, обычно используетс в url,
    # unique=True = говорится, что пол должны быть уникальным

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'  # Имя объекта во множ числе

    # class Meta - класс с некоторыми доп. данными, метаданными прикрепленнымик
    # модели он определяет, имя связанной таблицы данныхБ является ли модель
    # абстрактнойБ един или снож число модели


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    # PositiveSmallIntegerField Допускает число от 0 до 32767
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    # ImageField проверяет допускается загруженный объект допустимый к изображениям,
    # в upload_to указывается директория куда будем загружать изображения

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug':self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режисеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Изображение', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2019)
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director')
    # ManyToManyField Отношение многие ко многим, указываем 1-ым аргументом модель,
    # 2-ым передается имя для поля
    # 3-им - имя используемое для отношения связываемого объекта
    actors = models.ManyToManyField(Actor, verbose_name='актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField('Примьера в мире', default=date.today)
    budget = models.PositiveSmallIntegerField('Бюджет', default=0, help_text='Указать сумму в долларах')
    fees_in_usa = models.PositiveSmallIntegerField(
        'Сборы в США', default=0, help_text='Указать сумму в долларах'
    )
    fees_in_world = models.PositiveSmallIntegerField(
        'Сборы в мире', default=0, help_text='Указать сумму в долларах'
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})
        # Взято из url.py name (первый аргумент, kwargs - ключ взят из url.py, а значение из модели с полем url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movies_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    """ Рейтинг """
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )  # blank=True - означает, что поле не обязательно для заполнения
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

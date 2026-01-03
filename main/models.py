from django.db import models
from users.models import CustomUser

class AgeRating(models.Model):
    age_rating = models.CharField(max_length=10, unique=True, verbose_name='Возрастной рейтинг')
    min_age = models.SmallIntegerField(verbose_name='Минимальный возраст')
    
    class Meta:
        verbose_name = 'Возрастной рейтинг'
        verbose_name_plural = 'Возрастные рейтинги'
    
    def __str__(self):
        return self.age_rating

class Genre(models.Model):
    genre = models.CharField(max_length=30, unique=True, verbose_name='Жанр')
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.genre

class HallType(models.Model):
    hall_type = models.CharField(max_length=20, unique=True, verbose_name='Тип зала')
    
    class Meta:
        verbose_name = 'Тип кинозала'
        verbose_name_plural = 'Типы кинозалов'
    
    def __str__(self):
        return self.hall_type

class CinemaHall(models.Model):
    hall_type = models.ForeignKey(HallType, on_delete=models.RESTRICT, verbose_name='Тип зала')
    row_number = models.SmallIntegerField(verbose_name='Количество рядов')
    seat_number_in_row = models.SmallIntegerField(verbose_name='Мест в ряду')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    
    class Meta:
        verbose_name = 'Кинозал'
        verbose_name_plural = 'Кинозалы'
    
    def total_seats(self):
        return self.row_number * self.seat_number_in_row
    
    def __str__(self):
        return f"Зал {self.id} ({self.hall_type})"

class Movie(models.Model):
    age_rating = models.ForeignKey(AgeRating, on_delete=models.RESTRICT, verbose_name='Возрастной рейтинг')
    name = models.CharField(max_length=100, verbose_name='Название')
    duration = models.SmallIntegerField(verbose_name='Длительность (мин)')
    release_year = models.SmallIntegerField(blank=True, null=True, verbose_name='Год выпуска')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='Рейтинг')
    genres = models.ManyToManyField(Genre, through='MovieGenre', verbose_name='Жанры')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name='Постер')
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
    
    def __str__(self):
        return self.name
    @property
    def poster_url(self):
        if self.poster:
            return self.poster.url
        return '/static/img/no_poster.jpg'

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'genre')
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильмов'

class Session(models.Model):
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name='Кинозал')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    date_session = models.DateField(verbose_name='Дата сеанса')
    start_time = models.TimeField(verbose_name='Время начала')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    report = models.TextField(blank=True, null=True, verbose_name='Отчет')
    
    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
        ordering = ['date_session', 'start_time']
    
    def __str__(self):
        return f"{self.movie} - {self.date_session} {self.start_time}"

class Seat(models.Model):
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name='Кинозал')
    row = models.SmallIntegerField(verbose_name='Ряд')
    seat_in_row = models.SmallIntegerField(verbose_name='Место в ряду')
    
    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        unique_together = ('cinema_hall', 'row', 'seat_in_row')
    
    def __str__(self):
        return f"Ряд {self.row}, Место {self.seat_in_row}"

class Ticket(models.Model):
    STATUS_CHOICES = (
        (True, 'Продан'),
        (False, 'Свободен'),
    )
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Сеанс')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='Место')
    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Клиент')
    status = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')
    buy_date = models.DateField(blank=True, null=True, verbose_name='Дата покупки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        unique_together = ('session', 'seat')
    
    def __str__(self):
        return f"Билет #{self.id} - {self.session}"
from django.contrib import admin
from .models import *

@admin.register(AgeRating)
class AgeRatingAdmin(admin.ModelAdmin):
    list_display = ('age_rating', 'min_age')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)

@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ('hall_type',)

@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'hall_type', 'row_number', 'seat_number_in_row', 'available', 'total_seats')
    list_filter = ('hall_type', 'available')

class MovieGenreInline(admin.TabularInline):
    model = MovieGenre
    extra = 1

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_rating', 'duration', 'release_year', 'rating')
    list_filter = ('age_rating', 'genres')
    search_fields = ('name',)
    inlines = [MovieGenreInline]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema_hall', 'date_session', 'start_time', 'price')
    list_filter = ('date_session', 'cinema_hall')
    date_hierarchy = 'date_session'

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('cinema_hall', 'row', 'seat_in_row')
    list_filter = ('cinema_hall',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'seat', 'client', 'status', 'buy_date')
    list_filter = ('status', 'session__date_session')
    search_fields = ('client__username', 'client__email')
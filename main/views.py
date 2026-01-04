from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import *

def index(request):
    movies = Movie.objects.all()[:8]
    upcoming_sessions = Session.objects.filter(
        date_session__gte=timezone.now().date()
    ).order_by('date_session', 'start_time')[:10]
    
    context = {
        'movies': movies,
        'upcoming_sessions': upcoming_sessions,
    }
    return render(request, 'main/index.html', context)

def movie_list(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    age_ratings = AgeRating.objects.all()
    genre_filter = request.GET.get('genre')
    if genre_filter:
        movies = movies.filter(genres__id=genre_filter)
    
    age_rating_filter = request.GET.get('age_rating')
    if age_rating_filter:
        movies = movies.filter(age_rating_id=age_rating_filter)
    sort_by = request.GET.get('sort', 'name')
    allowed_sorts = ['name', '-name', '-rating', '-release_year']
    if sort_by not in allowed_sorts:
        sort_by = 'name'
    movies = movies.order_by(sort_by)
    context = {
        'movies': movies,
        'genres': genres,
        'age_ratings':age_ratings,
    }
    return render(request, 'main/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    sessions = Session.objects.filter(movie=movie, date_session__gte=timezone.now().date())
    
    context = {
        'movie': movie,
        'sessions': sessions,
    }
    return render(request, 'main/movie_detail.html', context)

def session_list(request):
    date_filter = request.GET.get('date')
    movie_filter = request.GET.get('movie')
    
    sessions = Session.objects.filter(date_session__gte=timezone.now().date())
    
    if date_filter:
        sessions = sessions.filter(date_session=date_filter)
    if movie_filter:
        sessions = sessions.filter(movie__id=movie_filter)
    
    movies = Movie.objects.all()
    
    context = {
        'sessions': sessions.order_by('date_session', 'start_time'),
        'movies': movies,
    }
    return render(request, 'main/session_list.html', context)

def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    tickets = Ticket.objects.filter(session=session).select_related('seat')
    
    seats_dict = {}
    for ticket in tickets:
        key = f"{ticket.seat.row}_{ticket.seat.seat_in_row}"
        seats_dict[key] = ticket
    
    context = {
        'session': session,
        'seats_dict': seats_dict,  # Простой словарь
        'rows_range': range(1, session.cinema_hall.row_number + 1),
        'seats_range': range(1, session.cinema_hall.seat_number_in_row + 1),
        'total_seats': session.cinema_hall.row_number * session.cinema_hall.seat_number_in_row,
        'available_seats': session.cinema_hall.row_number * session.cinema_hall.seat_number_in_row - tickets.count(),
        }
    return render(request, 'main/session_detail.html', context)

@login_required
def buy_ticket(request, session_id, seat_id=None):
    session = get_object_or_404(Session, id=session_id)
    
    if seat_id:
        seat = get_object_or_404(Seat, id=seat_id)
        existing_ticket = Ticket.objects.filter(session=session, seat=seat).first()
        if existing_ticket and existing_ticket.status:
            return redirect('main:session_detail', session_id=session_id)

        ticket = Ticket.objects.create(
            session=session,
            seat=seat,
            client=request.user,
            status=True,
            buy_date=timezone.now().date()
        )
        return redirect('main:ticket_detail', ticket_id=ticket.id)
    
    return redirect('main:session_detail', session_id=session_id)

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(client=request.user, status=True).select_related('session', 'seat')
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'main/my_tickets.html', context)

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if not request.user.is_staff and ticket.client != request.user:
        return redirect('main:index')
    
    context = {
        'ticket': ticket,
    }
    return render(request, 'main/ticket_detail.html', context)

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_staff):
            return function(request, *args, **kwargs)
        else:
            return redirect('main:index') 
    return wrap

@login_required
@admin_required
def admin_dashboard(request):
    stats = {
        'total_movies': Movie.objects.count(),
        'total_sessions': Session.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'total_users': CustomUser.objects.count(),
        'total_halls': CinemaHall.objects.filter(available=True).count(),
    }
    recent_tickets = Ticket.objects.select_related(
        'session', 'session__movie', 'client'
    ).order_by('-buy_date', '-id')[:10]
    
    context = {
        'stats': stats,
        'recent_tickets': recent_tickets,
    }
    return render(request, 'main/admin_dashboard.html', context)
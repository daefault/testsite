from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import *
import json

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
    hall_type_filter = request.GET.get('hall_type')  
    
    sessions = Session.objects.filter(date_session__gte=timezone.now().date())
    
    if date_filter:
        sessions = sessions.filter(date_session=date_filter)
    if movie_filter:
        sessions = sessions.filter(movie__id=movie_filter)
    if hall_type_filter:
        sessions = sessions.filter(cinema_hall__hall_type__id=hall_type_filter)
    
    sessions_by_date = dict()
    for session in sessions.order_by('date_session', 'start_time'):
        date_str = session.date_session.strftime('%Y-%m-%d')
        if date_str not in sessions_by_date:
            sessions_by_date[date_str] = []
        sessions_by_date[date_str].append(session)
  
    movies = Movie.objects.all()
    hall_types = HallType.objects.all() 
    
    context = {
        'sessions_by_date': sessions_by_date,
        'movies': movies,
        'hall_types': hall_types, 
    }
    return render(request, 'main/session_list.html', context)

def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    tickets = Ticket.objects.filter(session=session).select_related('seat')
    
    seats_matrix = []
    for row in range(1, session.cinema_hall.row_number + 1):
        row_seats = []
        for seat_num in range(1, session.cinema_hall.seat_number_in_row + 1):
            is_taken = any(
                t.seat.row == row and t.seat.seat_in_row == seat_num 
                for t in tickets
            )
            # ВАЖНО: Добавляем seat_key в формате "ряд_место"
            seat_key = f"{row}_{seat_num}"
            
            row_seats.append({
                'number': seat_num,
                'is_taken': is_taken,
                'row': row,
                'seat_num': seat_num,
                'seat_key': seat_key  # ДОБАВЛЕНО ЭТО!
            })
        seats_matrix.append({
            'row_number': row,
            'seats': row_seats
        })
    
    context = {
        'session': session,
        'seats_matrix': seats_matrix, 
        'total_seats': session.cinema_hall.row_number * session.cinema_hall.seat_number_in_row,
        'available_seats': session.cinema_hall.row_number * session.cinema_hall.seat_number_in_row - tickets.count(),
    }
    return render(request, 'main/session_detail.html', context)

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(client=request.user).select_related('session', 'seat').order_by('buy_date')
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

@login_required
def buy_multiple_tickets(request, session_id):
    """Покупка билетов для МАТРИЧНОЙ системы"""
    print("🎫 ПОКУПКА БИЛЕТОВ (МАТРИЦА)")
    print("🔍 Пользователь:", request.user.username)
    print("🔍 Метод запроса:", request.method)
    
    if request.method == 'POST':
        session_obj = get_object_or_404(Session, id=session_id)
        print(f"📽️ Сеанс: {session_obj.movie.name}")
        print(f"🏛️ Зал ID: {session_obj.cinema_hall.id}")
        
        # Получаем данные
        selected_seats_json = request.POST.get('selected_seats', '[]')
        print(f"📦 Получен JSON строка: {selected_seats_json}")
        print(f"📦 Тип данных: {type(selected_seats_json)}")
        print("🔍 Все POST данные:", dict(request.POST))
        
        try:
            # Убираем возможные лишние кавычки и пробелы
            selected_seats_json = selected_seats_json.strip()
            
            # Если строка начинается и заканчивается одинарными кавычками, убираем их
            if selected_seats_json.startswith("'") and selected_seats_json.endswith("'"):
                selected_seats_json = selected_seats_json[1:-1]
                print(f"📦 Убрали одинарные кавычки: {selected_seats_json}")
            
            # Декодируем JSON
            seat_keys = json.loads(selected_seats_json)
            print(f"🔑 Места из JSON: {seat_keys}")
            print(f"🔑 Тип: {type(seat_keys)}")
            print(f"🔑 Количество мест: {len(seat_keys)}")
            
            # Фильтруем None, null и пустые значения
            valid_seat_keys = []
            for key in seat_keys:
                if key is not None and key != 'null' and key != '':
                    valid_seat_keys.append(key)
            
            print(f"🔑 После фильтрации: {valid_seat_keys}")
            
            if not valid_seat_keys:
                print("❌ Нет мест для покупки после фильтрации")
                return redirect('main:session_detail', session_id=session_id)
            
            created_tickets = []
            
            for i, seat_key in enumerate(valid_seat_keys):
                print(f"\n🪑 [{i+1}] Обрабатываем ключ: '{seat_key}'")
                
                # Проверяем, что ключ - строка
                if not isinstance(seat_key, str):
                    print(f"   ❌ Ключ не строка: {type(seat_key)}")
                    continue
                
                # Ключ должен быть в формате "ряд_место"
                if '_' not in seat_key:
                    print(f"   ❌ Некорректный формат, нет '_'")
                    continue
                
                try:
                    row_str, seat_num_str = seat_key.split('_')
                    row = int(row_str.strip())
                    seat_num = int(seat_num_str.strip())
                    
                    print(f"   📍 Ряд: {row}, Место: {seat_num}")
                    
                    # Ищем место в зале этого сеанса
                    seats = Seat.objects.filter(
                        cinema_hall=session_obj.cinema_hall,
                        row=row,
                        seat_in_row=seat_num
                    )
                    
                    if not seats.exists():
                        print(f"   ❌ Место не найдено в зале {session_obj.cinema_hall.id}")
                        print(f"   🔍 Ищем: row={row}, seat_in_row={seat_num}")
                        
                        # Создаем место, если его нет
                        seat = Seat.objects.create(
                            cinema_hall=session_obj.cinema_hall,
                            row=row,
                            seat_in_row=seat_num
                        )
                        print(f"   ✅ Создано новое место (ID: {seat.id})")
                    else:
                        seat = seats.first()
                        print(f"   ✅ Место найдено (ID: {seat.id})")
                    
                    # Проверяем не занято ли
                    if Ticket.objects.filter(session=session_obj, seat=seat).exists():
                        print(f"   ⚠️ Место уже занято")
                        continue
                    
                    # Создаем билет
                    ticket = Ticket.objects.create(
                        session=session_obj,
                        seat=seat,
                        client=request.user,
                        status=False,
                        buy_date=timezone.now().date()
                    )
                    created_tickets.append(ticket)
                    print(f"   🎫 Билет создан (ID: {ticket.id})")
                    
                except ValueError as e:
                    print(f"   ❌ Ошибка преобразования: {e}")
                except Exception as e:
                    print(f"   ❌ Ошибка: {e}")
                    import traceback
                    traceback.print_exc()
            
            print(f"\n📊 ИТОГО: создано {len(created_tickets)} билетов")
            
            if created_tickets:
                return redirect('main:my_tickets')
            else:
                return redirect('main:session_detail', session_id=session_id)
                
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка JSON: {e}")
            print(f"❌ Ошибочная строка: {selected_seats_json}")
            return redirect('main:session_detail', session_id=session_id)
    
    print("❌ Не POST запрос")
    return redirect('main:session_detail', session_id=session_id)
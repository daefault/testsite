import os
import django
import random
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()
from main.models import *
from users.models import CustomUser

def create_age_ratings():
    """Создаем возрастные рейтинги"""
    ratings = [
        {'age_rating': '0+', 'min_age': 0},
        {'age_rating': '6+', 'min_age': 6},
        {'age_rating': '12+', 'min_age': 12},
        {'age_rating': '16+', 'min_age': 16},
        {'age_rating': '18+', 'min_age': 18},
    ]
    
    for r in ratings:
        AgeRating.objects.get_or_create(
            age_rating=r['age_rating'],
            defaults={'min_age': r['min_age']}
        )
    print(f"✅ Создано возрастных рейтингов: {len(ratings)}")
    return AgeRating.objects.all()

def create_hall_types():
    """Создаем типы залов"""
    types = ['2D', '3D', 'IMAX', 'VIP']
    
    for t in types:
        HallType.objects.get_or_create(hall_type=t)
    print(f"✅ Создано типов залов: {len(types)}")
    return HallType.objects.all()

def create_genres():
    """Создаем жанры"""
    genres = [
        'Фантастика', 'Боевик', 'Драма', 'Комедия', 
        'Триллер', 'Приключения', 'Ужасы', 'Мелодрама',
        'Мультфильм'
    ]
    
    for g in genres:
        Genre.objects.get_or_create(genre=g)
    print(f"✅ Создано жанров: {len(genres)}")
    return Genre.objects.all()

def create_cinema_halls():
    """Создаем кинозалы - ОПТИМИЗИРОВАННОЕ КОЛИЧЕСТВО"""
    halls = [
        {'type': '2D', 'rows': 8, 'seats': 10},    
        {'type': '3D', 'rows': 6, 'seats': 8},     
        {'type': 'IMAX', 'rows': 4, 'seats': 6},   
        {'type': 'VIP', 'rows': 3, 'seats': 4},   
    ]
    
    created = 0
    for hall in halls:
        hall_type, _ = HallType.objects.get_or_create(hall_type=hall['type'])
        cinema_hall, created_flag = CinemaHall.objects.get_or_create(
            hall_type=hall_type,
            row_number=hall['rows'],
            seat_number_in_row=hall['seats'],
            defaults={'available': True}
        )
        if created_flag:
            created += 1
    
    print(f"✅ Создано кинозалов: {created}")
    return CinemaHall.objects.all()

def create_movies():
    """Создаем фильмы - 10 фильмов для демонстрации"""
    movies = [
        {
            'name': 'Интерстеллар',
            'duration': 169,
            'year': 2014,
            'rating': 8.6,
            'age': '12+',
            'genres': ['Фантастика', 'Драма'],
            'desc': 'Путешествие через червоточину в поисках нового дома для человечества.'
        },
        {
            'name': 'Начало',
            'duration': 148,
            'year': 2010,
            'rating': 8.7,
            'age': '12+',
            'genres': ['Фантастика', 'Боевик'],
            'desc': 'Воры, крадущие идеи из снов.'
        },
        {
            'name': 'Король Лев',
            'duration': 88,
            'year': 1994,
            'rating': 8.8,
            'age': '0+',
            'genres': ['Мультфильм', 'Драма'],
            'desc': 'История львенка Симбы.'
        },
        {
            'name': 'Матрица',
            'duration': 136,
            'year': 1999,
            'rating': 8.7,
            'age': '16+',
            'genres': ['Фантастика', 'Боевик'],
            'desc': 'Хакер Нео discovers the truth about reality.'
        },
        {
            'name': 'Титаник',
            'duration': 194,
            'year': 1997,
            'rating': 8.4,
            'age': '12+',
            'genres': ['Драма', 'Мелодрама'],
            'desc': 'История любви на тонущем корабле.'
        },
        {
            'name': 'Властелин колец: Братство кольца',
            'duration': 178,
            'year': 2001,
            'rating': 8.8,
            'age': '12+',
            'genres': ['Фэнтези', 'Приключения'],
            'desc': 'Эпическое фэнтези о кольце всевластия.'
        },
        {
            'name': 'Криминальное чтиво',
            'duration': 154,
            'year': 1994,
            'rating': 8.9,
            'age': '18+',
            'genres': ['Криминал', 'Драма'],
            'desc': 'Переплетенные истории гангстеров.'
        },
        {
            'name': 'Один дома',
            'duration': 103,
            'year': 1990,
            'rating': 8.2,
            'age': '6+',
            'genres': ['Комедия'],
            'desc': 'Мальчик защищает дом от грабителей.'
        },
        {
            'name': 'Холодное сердце',
            'duration': 102,
            'year': 2013,
            'rating': 7.4,
            'age': '0+',
            'genres': ['Мультфильм', 'Фэнтези'],
            'desc': 'История Эльзы и Анны.'
        },
        {
            'name': 'Дюна',
            'duration': 155,
            'year': 2021,
            'rating': 8.0,
            'age': '12+',
            'genres': ['Фантастика', 'Драма'],
            'desc': 'Эпическая сага о пустынной планете.'
        },
    ]
    
    created = 0
    for m in movies:
        age_rating, _ = AgeRating.objects.get_or_create(
            age_rating=m['age'],
            defaults={'min_age': 12 if m['age'] == '12+' else 0 if m['age'] == '0+' else 16 if m['age'] == '16+' else 18}
        )
        
        movie, was_created = Movie.objects.get_or_create(
            name=m['name'],
            defaults={
                'age_rating': age_rating,
                'duration': m['duration'],
                'release_year': m['year'],
                'rating': m['rating'],
                'description': m['desc']
            }
        )
        
        if was_created:
            for genre_name in m['genres']:
                genre, _ = Genre.objects.get_or_create(genre=genre_name)
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)
            created += 1
    
    print(f"✅ Создано фильмов: {created}")
    return Movie.objects.all()

def create_users():
    """Создаем пользователей - достаточно для тестирования"""
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            email='admin@cinema.ru',
            password='admin123'
        )
        print("✅ Создан суперпользователь: admin / admin123")
    
    users = [
        {'username': 'user1', 'email': 'user1@mail.ru', 'password': '123456', 'role': 'user'},
        {'username': 'user2', 'email': 'user2@mail.ru', 'password': '123456', 'role': 'user'},
        {'username': 'manager', 'email': 'manager@cinema.ru', 'password': 'manager123', 'role': 'admin'},
        {'username': 'user3', 'email': 'user3@mail.ru', 'password': '123456', 'role': 'user'},
    ]
    
    created = 0
    for u in users:
        if not CustomUser.objects.filter(username=u['username']).exists():
            CustomUser.objects.create_user(
                username=u['username'],
                email=u['email'],
                password=u['password'],
                role=u['role']
            )
            created += 1
    
    print(f"✅ Создано пользователей: {created}")
    return CustomUser.objects.all()

def create_seats():
    """Создаем места в залах"""
    halls = CinemaHall.objects.all()
    total_seats = 0
    
    for hall in halls:
        existing_seats = Seat.objects.filter(cinema_hall=hall).count()
        if existing_seats > 0:
            total_seats += existing_seats
            continue
        
        seats = []
        for row in range(1, hall.row_number + 1):
            for seat_num in range(1, hall.seat_number_in_row + 1):
                seats.append(Seat(
                    cinema_hall=hall,
                    row=row,
                    seat_in_row=seat_num
                ))
        
        if seats:
            Seat.objects.bulk_create(seats)
            total_seats += len(seats)
    
    print(f"✅ Создано мест: {total_seats}")
    return total_seats

def create_sessions():
    """Создаем сеансы на декабрь 2025 и февраль 2026"""
    movies = list(Movie.objects.all())
    halls = list(CinemaHall.objects.filter(available=True))
    
    if not movies or not halls:
        print("❌ Нет данных для создания сеансов")
        return 0
    
    # Времена сеансов
    session_times = [
        '10:00', '13:00', '16:00', '19:00', '22:00'
    ]
    
    created = 0
    
    # Создаем сеансы на декабрь 2025 (прошедшие) - ТОЛЬКО 7 ДНЕЙ
    december_2025_start = datetime(2025, 12, 1).date()
    
    for day_offset in range(0, 7):  # Только 7 дней декабря
        date = december_2025_start + timedelta(days=day_offset)
        
        # Для каждого дня создаем по 1 сеансу в рандомном зале
        hall = random.choice(halls)
        time = random.choice(session_times)
        movie = random.choice(movies)
        
        # Простая логика цены
        price = 300
        if hall.hall_type.hall_type == '3D':
            price = 400
        elif hall.hall_type.hall_type == 'IMAX':
            price = 500
        elif hall.hall_type.hall_type == 'VIP':
            price = 600
        
        # Корректировка по времени
        hour = int(time.split(':')[0])
        if hour <= 12:
            price = int(price * 0.9)
        elif hour >= 22:
            price = int(price * 0.85)
        
        Session.objects.create(
            cinema_hall=hall,
            movie=movie,
            date_session=date,
            start_time=time,
            price=price
        )
        created += 1
    
    # Создаем сеансы на февраль 2026 (будущие) - ТОЛЬКО 7 ДНЕЙ
    february_2026_start = datetime(2026, 2, 1).date()
    
    for day_offset in range(0, 7):  # Только 7 дней февраля
        date = february_2026_start + timedelta(days=day_offset)
        
        # Для каждого дня создаем по 1 сеансу в рандомном зале
        hall = random.choice(halls)
        time = random.choice(session_times)
        movie = random.choice(movies)
        
        # Простая логика цены
        price = 300
        if hall.hall_type.hall_type == '3D':
            price = 400
        elif hall.hall_type.hall_type == 'IMAX':
            price = 500
        elif hall.hall_type.hall_type == 'VIP':
            price = 600
        
        # Корректировка по времени
        hour = int(time.split(':')[0])
        if hour <= 12:
            price = int(price * 0.9)
        elif hour >= 22:
            price = int(price * 0.85)
        
        Session.objects.create(
            cinema_hall=hall,
            movie=movie,
            date_session=date,
            start_time=time,
            price=price
        )
        created += 1
    
    print(f"✅ Создано сеансов: {created}")
    print(f"📅 Сеансы созданы на декабрь 2025 (7 дней) и февраль 2026 (7 дней)")
    return created

def create_tickets():
    """Создаем билеты - МАЛЕНЬКОЕ КОЛИЧЕСТВО для пользователей"""
    users = list(CustomUser.objects.filter(role='user'))
    
    if not users:
        print("❌ Нет пользователей для создания билетов")
        return 0
    
    # Распределим билеты между пользователями
    # user1 - 10 билетов (6 использованных, 4 активных)
    # user2 - 8 билетов (4 использованных, 4 активных)
    # user3 - 6 билетов (3 использованных, 3 активных)
    
    users_with_tickets = [
        {'user': users[0], 'total': 10, 'used': 6, 'active': 4},  # user1
        {'user': users[1], 'total': 8, 'used': 4, 'active': 4},   # user2
        {'user': users[2], 'total': 6, 'used': 3, 'active': 3},   # user3
    ]
    
    created = 0
    
    # Собираем все сеансы для создания билетов
    december_sessions = list(Session.objects.filter(date_session__year=2025, date_session__month=12))
    february_sessions = list(Session.objects.filter(date_session__year=2026, date_session__month=2))
    
    for user_data in users_with_tickets:
        user = user_data['user']
        
        # Создаем использованные билеты (на декабрь 2025)
        for i in range(user_data['used']):
            if not december_sessions:
                continue
                
            session = random.choice(december_sessions)
            seats = list(Seat.objects.filter(cinema_hall=session.cinema_hall))
            
            if not seats:
                continue
            
            # Ищем свободное место
            booked_seat_ids = Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
            available_seats = [s for s in seats if s.id not in booked_seat_ids]
            
            if not available_seats:
                continue
            
            seat = random.choice(available_seats)
            
            Ticket.objects.create(
                session=session,
                seat=seat,
                client=user,
                status=True,  # Использован
                buy_date=session.date_session - timedelta(days=random.randint(1, 14))
            )
            created += 1
        
        # Создаем активные билеты (на февраль 2026)
        for i in range(user_data['active']):
            if not february_sessions:
                continue
                
            session = random.choice(february_sessions)
            seats = list(Seat.objects.filter(cinema_hall=session.cinema_hall))
            
            if not seats:
                continue
            
            # Ищем свободное место
            booked_seat_ids = Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
            available_seats = [s for s in seats if s.id not in booked_seat_ids]
            
            if not available_seats:
                continue
            
            seat = random.choice(available_seats)
            
            Ticket.objects.create(
                session=session,
                seat=seat,
                client=user,
                status=False,  # Активен (не использован)
                buy_date=session.date_session - timedelta(days=random.randint(0, 7))
            )
            created += 1
        
        print(f"   • {user.username}: {user_data['total']} билетов ({user_data['used']} использованных, {user_data['active']} активных)")
    
    print(f"✅ Создано билетов: {created}")
    print(f"   • Всего у пользователей: {created} билетов")
    print(f"   • На декабрь 2025: {Ticket.objects.filter(session__date_session__year=2025, session__date_session__month=12).count()}")
    print(f"   • На февраль 2026: {Ticket.objects.filter(session__date_session__year=2026, session__date_session__month=2).count()}")
    
    return created

def main():
    """Основная функция"""
    print("=" * 50)
    print("🎬 ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ КИНОТЕАТРА")
    print("   (Версия с малым количеством билетов)")
    print("=" * 50)
    
    try:
        print("\n⚙️  Настройка заполнения базы данных:")
        print("1 - Очистить всё и заполнить заново")
        print("2 - Добавить к существующим данным")
        print("3 - Отмена")
        
        choice = input("\nТвой выбор (1/2/3): ").strip()
        
        if choice == '3':
            print("❌ Отменено")
            return
        
        if choice == '1':
            print("\n🧹 Очистка старых данных...")
            Ticket.objects.all().delete()
            Session.objects.all().delete()
            Seat.objects.all().delete()
            MovieGenre.objects.all().delete()
            Movie.objects.all().delete()
            CinemaHall.objects.all().delete()
            AgeRating.objects.all().delete()
            HallType.objects.all().delete()
            Genre.objects.all().delete()
            CustomUser.objects.filter(is_superuser=False).delete()
            print("✅ Старые данные удалены")
        
        print("\n🚀 Создание данных...")
        print("-" * 50)
        
        create_age_ratings()
        create_hall_types()
        create_genres()
        create_cinema_halls()
        create_movies()
        create_users()
        create_seats()
        create_sessions()
        create_tickets()
        
        print("\n" + "=" * 50)
        print("✅ ГОТОВО! Все функции доступны для тестирования")
        print("=" * 50)
        
        # Краткая статистика
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   • Фильмы: {Movie.objects.count()}")
        print(f"   • Кинозалы: {CinemaHall.objects.count()}")
        print(f"   • Сеансы: {Session.objects.count()}")
        print(f"   • Билеты: {Ticket.objects.count()}")
        print(f"   • Пользователи: {CustomUser.objects.count()}")
        
        # Статистика по билетам пользователей
        print(f"\n🎫 БИЛЕТЫ ПОЛЬЗОВАТЕЛЕЙ:")
        users = CustomUser.objects.filter(role='user')
        for user in users:
            tickets = Ticket.objects.filter(client=user)
            used = tickets.filter(status=True).count()
            active = tickets.filter(status=False).count()
            print(f"   • {user.username}: {tickets.count()} билетов ({used} использованных, {active} активных)")
        
        print(f"\n🔑 ДОСТУПНЫЕ АККАУНТЫ:")
        print(f"   • Админ: admin / admin123")
        print(f"   • Менеджер: manager / manager123")
        print(f"   • Пользователи:")
        print(f"       - user1 / 123456 (10 билетов)")
        print(f"       - user2 / 123456 (8 билетов)")
        print(f"       - user3 / 123456 (6 билетов)")
        
        print(f"\n📋 Для тестирования:")
        print(f"   1. Войдите как user1, user2 или user3")
        print(f"   2. На странице 'Мои билеты' увидите свои билеты")
        print(f"   3. Билеты на февраль 2026 - активные")
        print(f"   4. Билеты на декабрь 2025 - использованные")
        
        print("\n" + "=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n❌ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
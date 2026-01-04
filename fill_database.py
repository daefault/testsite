# fill_database.py
"""
Скрипт для заполнения базы данных тестовыми данными.
Просто положи этот файл в корень проекта (рядом с manage.py) и запусти:
python fill_database.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Настройка Django (ОБЯЗАТЕЛЬНО!)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()

# Теперь импортируем модели
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
        'Мультфильм'  # Добавил этот жанр, т.к. он используется в данных
    ]
    
    for g in genres:
        Genre.objects.get_or_create(genre=g)
    print(f"✅ Создано жанров: {len(genres)}")
    return Genre.objects.all()

def create_cinema_halls():
    """Создаем кинозалы"""
    halls = [
        {'type': '2D', 'rows': 10, 'seats': 15},
        {'type': '3D', 'rows': 8, 'seats': 12},
        {'type': 'IMAX', 'rows': 6, 'seats': 10},
        {'type': '2D', 'rows': 12, 'seats': 18},
        {'type': 'VIP', 'rows': 4, 'seats': 6},
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
    """Создаем фильмы"""
    # Сначала убедимся, что все жанры существуют
    genre_names = ['Фантастика', 'Боевик', 'Драма', 'Мелодрама', 'Мультфильм']
    for genre_name in genre_names:
        Genre.objects.get_or_create(genre=genre_name)
    
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
    ]
    
    created = 0
    for m in movies:
        # Получаем или создаем возрастной рейтинг
        age_rating, _ = AgeRating.objects.get_or_create(
            age_rating=m['age'],
            defaults={'min_age': 12 if m['age'] == '12+' else 0 if m['age'] == '0+' else 16}
        )
        
        # Создаем фильм
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
            # Добавляем жанры к фильму
            for genre_name in m['genres']:
                genre, _ = Genre.objects.get_or_create(genre=genre_name)
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)
            created += 1
    
    print(f"✅ Создано фильмов: {created}")
    return Movie.objects.all()

def create_users():
    """Создаем пользователей"""
    # Суперпользователь (админ Django)
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            email='admin@cinema.ru',
            password='admin123'
        )
        print("✅ Создан суперпользователь: admin / admin123")
    else:
        print("ℹ️  Суперпользователь admin уже существует")
    
    # Обычные пользователи
    users = [
        {'username': 'user1', 'email': 'user1@mail.ru', 'password': '123456', 'role': 'user'},
        {'username': 'user2', 'email': 'user2@mail.ru', 'password': '123456', 'role': 'user'},
        {'username': 'manager', 'email': 'manager@cinema.ru', 'password': 'manager123', 'role': 'admin'},
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
        # Проверяем, есть ли уже места
        existing_seats = Seat.objects.filter(cinema_hall=hall).count()
        if existing_seats > 0:
            print(f"ℹ️  В зале {hall.id} уже есть {existing_seats} мест, пропускаем")
            total_seats += existing_seats
            continue
        
        # Создаем новые места
        seats = []
        for row in range(1, hall.row_number + 1):
            for seat_num in range(1, hall.seat_number_in_row + 1):
                seats.append(Seat(
                    cinema_hall=hall,
                    row=row,
                    seat_in_row=seat_num
                ))
        
        # Используем bulk_create для эффективности
        if seats:
            Seat.objects.bulk_create(seats)
            total_seats += len(seats)
            print(f"✅ В зале {hall.id} создано {len(seats)} мест")
    
    print(f"✅ Всего мест в базе: {total_seats}")
    return total_seats

def create_sessions():
    """Создаем сеансы"""
    movies = Movie.objects.all()
    halls = CinemaHall.objects.filter(available=True)
    
    if not movies.exists():
        print("❌ Нет фильмов для создания сеансов")
        return 0
    if not halls.exists():
        print("❌ Нет доступных залов для создания сеансов")
        return 0
    
    # Сеансы на сегодня и завтра
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    sessions_data = [
        {'date': today, 'time': '10:00', 'price': 300},
        {'date': today, 'time': '13:00', 'price': 350},
        {'date': today, 'time': '16:00', 'price': 400},
        {'date': today, 'time': '19:00', 'price': 450},
        {'date': today, 'time': '22:00', 'price': 500},
        {'date': tomorrow, 'time': '11:00', 'price': 300},
        {'date': tomorrow, 'time': '14:00', 'price': 350},
        {'date': tomorrow, 'time': '17:00', 'price': 400},
        {'date': tomorrow, 'time': '20:00', 'price': 450},
        {'date': tomorrow, 'time': '23:00', 'price': 500},
    ]
    
    created = 0
    for session_data in sessions_data:
        movie = random.choice(list(movies))
        hall = random.choice(list(halls))
        
        # Проверяем, нет ли уже такого сеанса
        existing = Session.objects.filter(
            cinema_hall=hall,
            movie=movie,
            date_session=session_data['date'],
            start_time=session_data['time']
        ).exists()
        
        if not existing:
            Session.objects.create(
                cinema_hall=hall,
                movie=movie,
                date_session=session_data['date'],
                start_time=session_data['time'],
                price=session_data['price']
            )
            created += 1
    
    print(f"✅ Создано сеансов: {created}")
    return created

def create_tickets():
    """Создаем билеты"""
    sessions = Session.objects.all()
    users = CustomUser.objects.filter(role='user')
    
    if not sessions.exists():
        print("❌ Нет сеансов для создания билетов")
        return 0
    
    created = 0
    for session in sessions:
        # Берем места из этого зала
        seats = Seat.objects.filter(cinema_hall=session.cinema_hall)
        if not seats.exists():
            print(f"ℹ️  В зале {session.cinema_hall.id} нет мест, пропускаем")
            continue
        
        # Проверяем, сколько билетов уже есть на этот сеанс
        existing_tickets = Ticket.objects.filter(session=session).count()
        
        # Если уже много билетов, пропускаем
        if existing_tickets >= len(seats) * 0.5:  # 50% мест уже занято
            continue
        
        # Создаем 2-4 билета на сеанс
        num_tickets = random.randint(2, 4)
        available_seats = list(seats.exclude(
            id__in=Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
        ))
        
        if not available_seats:
            continue
            
        selected_seats = random.sample(
            available_seats, 
            min(num_tickets, len(available_seats))
        )
        
        for seat in selected_seats:
            # 70% билетов с пользователем, 30% без
            user = random.choice(list(users)) if random.random() < 0.7 and users.exists() else None
            
            Ticket.objects.create(
                session=session,
                seat=seat,
                client=user,
                status=True,  # Продан
                buy_date=session.date_session - timedelta(days=random.randint(0, 2))
            )
            created += 1
    
    print(f"✅ Создано билетов: {created}")
    return created

def main():
    """Основная функция - запускает всё"""
    print("=" * 50)
    print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ КИНОТЕАТРА")
    print("=" * 50)
    
    try:
        # Спрашиваем, нужно ли очистить старые данные
        print("\nХочешь очистить старые данные перед заполнением?")
        print("1 - Да, очистить всё")
        print("2 - Нет, добавить к существующим")
        print("3 - Отмена")
        
        choice = input("Твой выбор (1/2/3): ").strip()
        
        if choice == '3':
            print("❌ Отменено")
            return
        
        if choice == '1':
            print("\n🧹 Очистка старых данных...")
            # Удаляем в правильном порядке из-за внешних ключей
            Ticket.objects.all().delete()
            Session.objects.all().delete()
            Seat.objects.all().delete()
            MovieGenre.objects.all().delete()
            Movie.objects.all().delete()
            CinemaHall.objects.all().delete()
            AgeRating.objects.all().delete()
            HallType.objects.all().delete()
            Genre.objects.all().delete()
            # Не удаляем пользователей, чтобы не потерять админа
            print("✅ Старые данные удалены")
        
        print("\n🚀 Начинаем создание данных...")
        
        # Создаем данные по порядку (важен порядок!)
        create_age_ratings()
        create_hall_types()
        create_genres()  # Жанры должны быть созданы до фильмов!
        create_cinema_halls()
        create_movies()  # Теперь жанры уже существуют
        create_users()
        create_seats()
        create_sessions()
        create_tickets()
        
        print("\n" + "=" * 50)
        print("✅ ВСЁ ГОТОВО!")
        print("=" * 50)
        
        # Показываем итоги
        print(f"\n📊 Создано всего:")
        print(f"   • Фильмов: {Movie.objects.count()}")
        print(f"   • Кинозалов: {CinemaHall.objects.count()}")
        print(f"   • Сеансов: {Session.objects.count()}")
        print(f"   • Билетов: {Ticket.objects.count()}")
        print(f"   • Пользователей: {CustomUser.objects.count()}")
        
        print(f"\n🔑 Доступные логины:")
        print(f"   • Админ Django: admin / admin123")
        print(f"   • Менеджер кинотеатра: manager / manager123")
        print(f"   • Обычный пользователь: user1 / 123456")
        print(f"   • Обычный пользователь: user2 / 123456")
        
        print(f"\n🎬 Для входа в админку Django:")
        print(f"   Перейди по адресу: http://127.0.0.1:8000/admin/")
        print(f"   Логин: admin")
        print(f"   Пароль: admin123")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
if __name__ == '__main__':
    main()
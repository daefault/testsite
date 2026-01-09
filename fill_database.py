import os
import django
import random
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()
from main.models import *
from users.models import CustomUser

def create_age_ratings():
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
    return AgeRating.objects.all()

def create_hall_types():
    types = ['2D', '3D', 'IMAX', 'VIP']
    
    for t in types:
        HallType.objects.get_or_create(hall_type=t)
    return HallType.objects.all()

def create_genres():
    genres = [
        'Фантастика', 'Боевик', 'Драма', 'Комедия', 
        'Триллер', 'Приключения', 'Ужасы', 'Мелодрама',
        'Мультфильм'
    ]
    
    for g in genres:
        Genre.objects.get_or_create(genre=g)
    return Genre.objects.all()

def create_cinema_halls():
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
    
    return CinemaHall.objects.all()

def create_movies():
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
            'desc': 'Хакер Нео узнаёт правду о реальности.'
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
    
    return Movie.objects.all()

def create_users():
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            email='admin@cinema.ru',
            password='admin123'
        )
    
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
    
    return CustomUser.objects.all()

def create_seats():
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
    
    return total_seats

def create_sessions():
    movies = list(Movie.objects.all())
    halls = list(CinemaHall.objects.filter(available=True))
  
    session_times = [
        '10:00', '13:00', '16:00', '19:00', '22:00'
    ]
    
    created = 0
    
    december_2025_start = datetime(2025, 12, 1).date()
    
    for day_offset in range(0, 7):  
        date = december_2025_start + timedelta(days=day_offset)

        hall = random.choice(halls)
        time = random.choice(session_times)
        movie = random.choice(movies)

        price = 300
        if hall.hall_type.hall_type == '3D':
            price = 400
        elif hall.hall_type.hall_type == 'IMAX':
            price = 500
        elif hall.hall_type.hall_type == 'VIP':
            price = 600
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
    
    february_2026_start = datetime(2026, 2, 1).date()
    
    for day_offset in range(0, 7): 
        date = february_2026_start + timedelta(days=day_offset)
        
        hall = random.choice(halls)
        time = random.choice(session_times)
        movie = random.choice(movies)
        
        price = 300
        if hall.hall_type.hall_type == '3D':
            price = 400
        elif hall.hall_type.hall_type == 'IMAX':
            price = 500
        elif hall.hall_type.hall_type == 'VIP':
            price = 600
        
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
    
    return created

def create_tickets():
    users = list(CustomUser.objects.filter(role='user'))
    
    
    
    users_with_tickets = [
        {'user': users[0], 'total': 10, 'used': 6, 'active': 4},  
        {'user': users[1], 'total': 8, 'used': 4, 'active': 4},   
        {'user': users[2], 'total': 6, 'used': 3, 'active': 3},   
    ]
    
    created = 0
    december_sessions = list(Session.objects.filter(date_session__year=2025, date_session__month=12))
    february_sessions = list(Session.objects.filter(date_session__year=2026, date_session__month=2))
    
    for user_data in users_with_tickets:
        user = user_data['user']
        
        for i in range(user_data['used']):
            if not december_sessions:
                continue
                
            session = random.choice(december_sessions)
            seats = list(Seat.objects.filter(cinema_hall=session.cinema_hall))
            
            if not seats:
                continue
            
            booked_seat_ids = Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
            available_seats = [s for s in seats if s.id not in booked_seat_ids]
            
            if not available_seats:
                continue
            
            seat = random.choice(available_seats)
            
            Ticket.objects.create(
                session=session,
                seat=seat,
                client=user,
                status=True,  
                buy_date=session.date_session - timedelta(days=random.randint(1, 14))
            )
            created += 1
        
        for i in range(user_data['active']):
            if not february_sessions:
                continue
                
            session = random.choice(february_sessions)
            seats = list(Seat.objects.filter(cinema_hall=session.cinema_hall))
            
            if not seats:
                continue
            

            booked_seat_ids = Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
            available_seats = [s for s in seats if s.id not in booked_seat_ids]
            
            if not available_seats:
                continue
            
            seat = random.choice(available_seats)
            
            Ticket.objects.create(
                session=session,
                seat=seat,
                client=user,
                status=False, 
                buy_date=session.date_session - timedelta(days=random.randint(0, 7))
            )
            created += 1
        
    
    
    return created

def main():
    
    print("\n⚙️  Настройка заполнения базы данных:")
    print("1 - Очистить всё и заполнить заново")
    print("2 - Добавить к существующим данным")
    print("3 - Отмена")
        
    choice = input("\nТвой выбор (1/2/3): ").strip()
        
    if choice == '3':
        return
        
    if choice == '1':
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
        
    create_age_ratings()
    create_hall_types()
    create_genres()
    create_cinema_halls()
    create_movies()
    create_users()
    create_seats()
    create_sessions()
    create_tickets()
        
    users = CustomUser.objects.filter(role='user')
    for user in users:
        tickets = Ticket.objects.filter(client=user)
        used = tickets.filter(status=True).count()
        active = tickets.filter(status=False).count()
        
        

if __name__ == '__main__':
    main()
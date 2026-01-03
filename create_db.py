import psycopg2
from psycopg2 import sql
import sys

def create_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='scripted57',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='cinemadb'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE cinemadb"))
            print("База данных 'cinemadb' создана успешно!")
        else:
            print("База данных 'cinemadb' уже существует.")
        
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname='postgres'")
        user_exists = cursor.fetchone()
        
        if not user_exists:
            cursor.execute(sql.SQL("CREATE USER postgres WITH PASSWORD 'scripted57'"))
            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE cinemadb TO postgres"))
            cursor.execute(sql.SQL("ALTER USER postgres CREATEDB"))
            print("Пользователь 'postgres' создан успешно!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
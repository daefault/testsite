import psycopg2
from psycopg2 import sql

def create_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='scripted57',
        host='localhost',
        port='5432'
        )
    conn.autocommit = True
    cursor = conn.cursor() 
    cursor.execute(sql.SQL("CREATE DATABASE cinemadb"))
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
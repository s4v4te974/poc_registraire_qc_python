import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/registraire')


def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:")
        print(e)

from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:h8wcwheJ7Y9t7Tw4DReU@containers-us-west-183.railway.app:6905/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_connection():
    try:
        connection = engine.connect()
        return connection
    except OperationalError:
        print("Connection failed, retrying")
        connection = engine.connect()
        return connection

import os
from typing import Any
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2

load_dotenv()
Base = declarative_base()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise RuntimeError("Missing required database environment variables")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing env var: {name}")
    return value

def get_db_connection():

    connection = psycopg2.connect(
        host=get_env("POSTGRES_HOST"),
        port=get_env("POSTGRES_PORT"),
        database=get_env("POSTGRES_DB"),
        user=get_env("POSTGRES_USER"),
        password=get_env("POSTGRES_PASSWORD")
    )
    return connection

def read_db(
        query: str,
        params=None)-> list[dict[str, Any]]:
    """
    Returns: A list of result as list of dictionaries.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = cursor.fetchall()
            return result

def write_db(
        query: str,
        params=None)-> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
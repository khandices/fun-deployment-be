import os
from typing import Any

import psycopg2


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing env var: {name}")
    return value

def get_db_connection():

    connection = psycopg2.connect(
        host=get_env("DB_HOST"),
        port=get_env("DB_PORT"),
        database=get_env("DB_NAME"),
        user=get_env("DB_USER"),
        password=get_env("DB_PASSWORD")
    )
    return connection

def read_db(
        query: str,
        params=None)-> list[tuple[Any, ...]]:
    """
    Returns: A list of result rows as tuples.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result

def write_db(
        query: str,
        params=None)-> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
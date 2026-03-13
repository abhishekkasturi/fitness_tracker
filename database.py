import psycopg2
import os


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        gym_code TEXT,
        username TEXT,
        password_hash TEXT,
        age INTEGER,
        sex TEXT,
        height REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(gym_code, username)
    )
    """)

    conn.commit()
    conn.close()
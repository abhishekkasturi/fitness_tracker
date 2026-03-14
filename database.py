import psycopg2
import os


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    # Users table
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

    # Weekly metrics table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weekly_metrics(
        id SERIAL PRIMARY KEY,

        user_id INTEGER REFERENCES users(id),

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        weight REAL,
        chest REAL,
        biceps REAL,
        waist REAL,
        thigh REAL,
        calf REAL,

        bench REAL,
        squat REAL,
        deadlift REAL,

        pushups INTEGER,
        pullups INTEGER,
        plank INTEGER,

        vo2max REAL,
        resting_hr INTEGER,
        hrv REAL
    )
    """)

    conn.commit()
    conn.close()
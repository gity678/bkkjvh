import os
import sqlite3

DB_DIR = "database"
DB_FILE = os.path.join(DB_DIR, "data.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start TEXT,
                duration INTEGER,
                final_duration INTEGER
            )
        ''')
        conn.commit()

def insert_timer(start, duration, final_duration):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO timers (start, duration, final_duration) VALUES (?, ?, ?)",
            (start, duration, final_duration)
        )
        conn.commit()

def fetch_all_timers():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM timers").fetchall()

def delete_timer(timer_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM timers WHERE id = ?", (timer_id,))
        conn.commit()

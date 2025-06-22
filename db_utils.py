import sqlite3

DB_FILE = "data.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start TEXT,
                duration INTEGER,
                final_duration INTEGER
            )
        ''')

def add_column_if_not_exists():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(timers)")
        columns = [col[1] for col in cursor.fetchall()]
        if "status" not in columns:
            cursor.execute("ALTER TABLE timers ADD COLUMN status TEXT DEFAULT 'active'")
            conn.commit()

def insert_timer(start, duration, final_duration):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO timers (start, duration, final_duration) VALUES (?, ?, ?)",
            (start, duration, final_duration)
        )
        conn.commit()

def delete_timer(timer_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM timers WHERE id = ?", (timer_id,))
        conn.commit()

def fetch_all_timers():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM timers").fetchall()

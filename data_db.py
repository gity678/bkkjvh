import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    "host": "your-mysql-host",
    "user": "your-username",
    "password": "your-password",
    "database": "your-database",
    "cursorclass": DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                start VARCHAR(255),
                duration INT,
                final_duration INT
            )
        ''')
    conn.commit()
    conn.close()

def insert_timer(start, duration, final_duration):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO timers (start, duration, final_duration) VALUES (%s, %s, %s)"
        cursor.execute(sql, (start, duration, final_duration))
    conn.commit()
    conn.close()

def fetch_all_timers():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM timers")
        results = cursor.fetchall()
    conn.close()
    return results

def delete_timer(timer_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM timers WHERE id = %s", (timer_id,))
    conn.commit()
    conn.close()

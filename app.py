from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.debug = True
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

def format_extended_duration(seconds):
    if seconds is None:
        return "--"
    duration = timedelta(seconds=seconds)
    days = duration.days
    hours, rem = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days} يوم")
    if hours: parts.append(f"{hours} ساعة")
    if minutes: parts.append(f"{minutes} دقيقة")
    if seconds or not parts: parts.append(f"{seconds} ثانية")
    return " ".join(parts)

init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        timers_raw = conn.execute("SELECT * FROM timers").fetchall()
        
        final_durations = [row["final_duration"] for row in timers_raw if row["final_duration"] is not None]

        count = len(final_durations)
        total = sum(final_durations) if final_durations else 0
        avg = total // count if count > 0 else 0
        max_d = max(final_durations) if final_durations else 0

        stats = {
            "count": count,
            "average": format_extended_duration(avg),
            "maximum": format_extended_duration(max_d)
        }

        timers = []
        for row in timers_raw:
            timers.append({
                "id": row["id"],
                "start": row["start"],
                "duration": row["duration"],
                "final_duration": row["final_duration"],
                "duration_str": format_extended_duration(row["duration"]),
                "final_str": format_extended_duration(row["final_duration"])
            })

        return render_template("index.html", timers=timers, stats=stats)

@app.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()
    try:
        start = data["start"]
        duration = int(data["duration"])
        final_duration = int(data["final_duration"])
    except (KeyError, ValueError, TypeError):
        return jsonify({"status": "error", "message": "بيانات غير صحيحة"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO timers (start, duration, final_duration) VALUES (?, ?, ?)",
                     (start, duration, final_duration))
        conn.commit()
    return jsonify({"status": "ok"})

@app.route("/delete/<int:id>", methods=["POST"])
def delete_timer(id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM timers WHERE id = ?", (id,))
        conn.commit()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

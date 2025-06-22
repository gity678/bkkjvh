from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_FILE = "data.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start TEXT,
                duration TEXT,
                final_duration TEXT
            )
        ''')
init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM timers").fetchall()
        return render_template("index.html", timers=rows)

@app.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT INTO timers (start, duration, final_duration)
            VALUES (?, ?, ?)
        ''', (data["start"], data["duration"], data["final_duration"]))
        conn.commit()
    return jsonify({"status": "تم الحفظ"})

@app.route("/delete/<int:id>", methods=["POST"])
def delete_timer(id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM timers WHERE id = ?", (id,))
        conn.commit()
    return jsonify({"status": "تم الحذف"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

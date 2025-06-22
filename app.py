from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_FILE = "data.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start TEXT,
                end TEXT,
                duration TEXT
            )
        ''')
init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM timers").fetchall()
        return render_template("index.html", timers=rows)

@app.route("/data", methods=["GET"])
def get_data():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM timers").fetchall()
        return jsonify([dict(row) for row in rows])

@app.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO timers (title, start, end, duration) VALUES (?, ?, ?, ?)",
                     (data["title"], data["start"], data["end"], data["duration"]))
        conn.commit()
    return jsonify({"status": "تمت الإضافة بنجاح"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

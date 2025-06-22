from flask import Flask, request, jsonify, render_template
from data_db import init_db, insert_timer, fetch_all_timers, delete_timer

app = Flask(__name__)
app.debug = True

def format_extended_duration(seconds):
    if seconds is None:
        return "--"
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days} يوم")
    if hours: parts.append(f"{hours} ساعة")
    if minutes: parts.append(f"{minutes} دقيقة")
    if seconds or not parts: parts.append(f"{seconds} ثانية")
    return " ".join(parts)

@app.route("/")
def index():
    timers_raw = fetch_all_timers()
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

    # حساب إحصائيات (مجموع، متوسط، أطول مدة)
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

    return render_template("index.html", timers=timers, stats=stats)

@app.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()
    start = data.get("start")
    duration = int(data.get("duration", 0))
    final_duration = int(data.get("final_duration", 0))
    insert_timer(start, duration, final_duration)
    return jsonify({"status": "ok"})

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    delete_timer(id)
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

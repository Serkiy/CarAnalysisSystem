from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "database.db"


def get_db():
    return sqlite3.connect(DB)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add-data", methods=["POST"])
def add_data():
    data = request.json

    speed = data.get("speed")
    rpm = data.get("rpm")
    temperature = data.get("temperature")  # optional

    if speed is None or rpm is None:
        return jsonify({"error": "invalid data"}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO car_data (speed, rpm, temperature, created_at)
        VALUES (?, ?, ?, ?)
    """, (speed, rpm, temperature, datetime.now()))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


@app.route("/data")
def data():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT speed, rpm, created_at
        FROM car_data
        ORDER BY created_at DESC
        LIMIT 50
    """)
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)

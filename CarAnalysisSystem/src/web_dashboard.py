from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

# Importăm funcția de analiză din celălalt fișier
from data_processor import analyze_car_data

app = Flask(__name__)
DB_PATH = 'car_analysis.db'

# --- INIȚIALIZARE BAZĂ DE DATE ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabel pentru datele Live (RPM, Speed, Temp)
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       rpm INTEGER, speed INTEGER, temp INTEGER, 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Tabel pentru istoricul recomandărilor (fără date brute, doar mesaj)
    cursor.execute('''CREATE TABLE IF NOT EXISTS recommendation_history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       rec_text TEXT, 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# --- INTERFAȚA DASHBOARD (HTML/CSS/JS) ---
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>OBD Dashboard Control</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #121212; color: white; margin: 0; display: flex; }
            nav { width: 260px; background: #1e1e1e; height: 100vh; padding: 20px; border-right: 1px solid #333; position: fixed; }
            main { margin-left: 300px; padding: 40px; width: calc(100% - 300px); }
            .nav-item { display: block; padding: 15px; color: #00adb5; text-decoration: none; cursor: pointer; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; }
            .nav-item:hover { background: #252525; color: #00fff2; }
            .section { display: none; }
            .active { display: block; }
            .card { background: #1e1e1e; padding: 30px; border-radius: 15px; border: 1px solid #333; text-align: center; }
            .data-val { font-size: 4em; font-weight: bold; margin: 10px 0; color: #00adb5; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e1e1e; }
            th, td { padding: 12px; border: 1px solid #333; text-align: left; }
            th { background: #00adb5; color: black; }
            tr:nth-child(even) { background: #252525; }
        </style>
    ++</head>
    <body>
        <nav>
            <h2 style="color:#00adb5">OBD SYSTEM</h2>
            <p style="font-size: 0.8em; color: #666;">Status Server: <span id="conn-status" style="color: green;">Activ</span></p>
            <hr style="border: 0.5px solid #333; margin: 20px 0;">
            <div class="nav-item" onclick="showSection('live')">DASHBOARD LIVE</div>
            <div class="nav-item" onclick="showSection('history')">ISTORIC DATE</div>
            <div class="nav-item" onclick="showSection('recs')">RECOMANDĂRI</div>
        </nav>

        <main>
            <div id="live" class="section active">
                <h1>Date Live din Obdmancamiar</h1>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="card"><h3>RPM</h3><div id="l-rpm" class="data-val">0</div></div>
                    <div class="card"><h3>VITEZĂ</h3><div id="l-speed" class="data-val">0</div><span>km/h</span></div>
                    <div class="card" style="grid-column: span 2;"><h3>TEMP. MOTOR</h3><div id="l-temp" class="data-val">0</div><span>°C</span></div>
                </div>
            </div>

            <div id="history" class="section">
                <h1>Istoric Date (Data Completă)</h1>
                <table id="table-logs">
                    <thead><tr><th>Timestamp</th><th>RPM</th><th>Viteza</th><th>Temp</th></tr></thead>
                    <tbody></tbody>
                </table>
            </div>

            <div id="recs" class="section">
                <h1>Sistem Recomandări</h1>
                <p>Recomandări bazate pe stilul de condus (stocate la fiecare 50 pachete de date).</p>
                <table id="table-recs">
                    <thead><tr><th>Data Generării</th><th>Mesaj Recomandare</th></tr></thead>
                    <tbody></tbody>
                </table>
            </div>
        </main>

        <script>
            function showSection(id) {
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.getElementById(id).classList.add('active');
                if(id === 'history') loadHistory();
                if(id === 'recs') loadRecs();
            }

            function updateLive() {
                fetch('/get-latest').then(r => r.json()).then(res => {
                    if(res.status === 'success') {
                        document.getElementById('l-rpm').innerText = res.data.rpm;
                        document.getElementById('l-speed').innerText = res.data.speed;
                        document.getElementById('l-temp').innerText = res.data.temp;
                    }
                });
            }

            function loadHistory() {
                fetch('/get-history').then(r => r.json()).then(data => {
                    let h = '';
                    data.forEach(row => { h += `<tr><td>${row[4]}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3]}</td></tr>`; });
                    document.querySelector('#table-logs tbody').innerHTML = h;
                });
            }

            function loadRecs() {
                fetch('/get-recs-history').then(r => r.json()).then(data => {
                    let h = '';
                    data.forEach(row => { h += `<tr><td>${row[2]}</td><td>${row[1]}</td></tr>`; });
                    document.querySelector('#table-recs tbody').innerHTML = h;
                });
            }
            setInterval(updateLive, 500);
        </script>
    </body>
    </html>
    """)

# --- RUTE API PENTRU REȚEA ---

@app.route('/add-data', methods=['POST'])
def add_data():
    try:
        content = request.json
        rpm = int(content.get('rpm', 0))
        speed = int(content.get('speed', 0))
        temp = int(content.get('temp', 0))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Salvare date brute
        cursor.execute("INSERT INTO logs (rpm, speed, temp) VALUES (?, ?, ?)", (rpm, speed, temp))
        
        # 2. Logică Recomandări (la fiecare 50 intrări)
        cursor.execute("SELECT COUNT(*) FROM logs")
        count = cursor.fetchone()[0]
        
        if count % 50 == 0:
            recoms = analyze_car_data(rpm, speed, temp)
            cursor.execute("INSERT INTO recommendation_history (rec_text) VALUES (?)", (recoms[0],))
            
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/get-latest')
def get_latest():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rpm, speed, temp FROM logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"status": "success", "data": {"rpm": row[0], "speed": row[1], "temp": row[2]}})
    return jsonify({"status": "error"})

@app.route('/get-history')
def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall(); conn.close()
    return jsonify(rows)

@app.route('/get-recs-history')
def get_recs_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recommendation_history ORDER BY id DESC")
    rows = cursor.fetchall(); conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    # Ascultă pe toate interfețele (important pentru conexiunea cu telefonul)
    app.run(host='0.0.0.0', port=5000)
import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS car_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    speed INTEGER,
    rpm INTEGER,
    temperature REAL,
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")

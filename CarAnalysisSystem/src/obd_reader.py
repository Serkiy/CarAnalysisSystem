import time
import sqlite3
import os
from datetime import datetime

class MockOBDReader:
    """Simulator OBD-II pentru testare"""
    
    def __init__(self):
        # Asigură-te că folderul data există
        if not os.path.exists('data'):
            os.makedirs('data')
        
        self.connection = sqlite3.connect('data/car_data.db')
        self.create_table()
    
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rpm INTEGER,
                speed INTEGER,
                engine_temp INTEGER,
                battery_voltage REAL,
                fuel_level INTEGER
            )
        ''')
        self.connection.commit()
        print("✅ Database table created successfully!")
    
    def read_obd_data(self):
        """Simulează citirea datelor de la OBD-II"""
        import random
        
        return {
            'rpm': random.randint(800, 3500),
            'speed': random.randint(0, 120),
            'engine_temp': random.randint(85, 105),
            'battery_voltage': round(random.uniform(12.5, 14.5), 2),
            'fuel_level': random.randint(10, 100)
        }
    
    def save_to_database(self, data):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO car_metrics (rpm, speed, engine_temp, battery_voltage, fuel_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['rpm'], data['speed'], data['engine_temp'], 
              data['battery_voltage'], data['fuel_level']))
        self.connection.commit()
        print(f"💾 Data saved: {data}")
    
    def start_monitoring(self):
        """Pornește monitorizarea continuă"""
        print("🚗 Starting car monitoring...")
        try:
            while True:
                data = self.read_obd_data()
                self.save_to_database(data)
                time.sleep(5)  # Citește la fiecare 5 secunde
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        finally:
            self.connection.close()

if __name__ == "__main__":
    reader = MockOBDReader()
    reader.start_monitoring()

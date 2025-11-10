# obd_test.py
import time
import random

class MockOBDConnection:
    """Simulează o conexiune OBD pentru testare"""
    
    def __init__(self, port=None):
        self.port_name = port or "MOCK_COM_PORT"
        self._connected = True
        
    def is_connected(self):
        return self._connected
        
    def query(self, command_type):
        """Simulează interogarea unui parametru OBD"""
        class MockResponse:
            def __init__(self, value):
                self.value = value
        
        # Simulează valorile în funcție de tipul de comandă
        if "RPM" in str(command_type):
            # RPM realist: 800-3500, cu variații simulate
            rpm_value = random.randint(800, 1200) if random.random() > 0.7 else random.randint(1500, 3500)
            return MockResponse(type('Quantity', (), {'magnitude': rpm_value})())
        
        elif "SPEED" in str(command_type):
            # Viteză realistă: 0-120 km/h
            speed_value = random.randint(0, 30) if random.random() > 0.6 else random.randint(40, 120)
            
            class SpeedValue:
                def __init__(self, speed):
                    self.magnitude = speed
                def to(self, unit):
                    return self  # Pentru compatibilitate cu codul original
            
            return MockResponse(SpeedValue(speed_value))
        
        else:
            # Pentru alte comenzi
            return MockResponse(type('Quantity', (), {'magnitude': 0})())
    
    def close(self):
        self._connected = False

def main():
    PORT = "COM6"  # sau None pentru autoconnect
    
    print(" OBD TEST - MOCK MODE")
    print(" Running in simulation mode (no hardware required)")
    
    if PORT:
        print(f" Simulating connection to port: {PORT}")
        conn = MockOBDConnection(PORT)
    else:
        print(" Simulating auto-detect connection...")
        conn = MockOBDConnection()

    if not conn.is_connected():
        print(" Mock connection failed (should not happen)")
        return

    print("Connected to:", conn.port_name)
    print("generating realistic car data...")

    try:
        for i in range(20):
            # Simulează citirea datelor
            r_rpm = conn.query("RPM")
            r_speed = conn.query("SPEED")

            # Procesează datele ca în codul original
            rpm = r_rpm.value.magnitude if (r_rpm.value is not None) else None
            
            speed = None
            if r_speed.value is not None:
                try:
                    speed = r_speed.value.to("km/h").magnitude
                except Exception:
                    speed = r_speed.value.magnitude

            # Afișează cu emoji pentru vizualizare mai bună
            print(f"[{i+1:2d}]  RPM: {rpm:4d} |  Speed: {speed:3d} km/h | ", end="")
            
            # Adaugă indicator vizual
            if speed == 0:
                print(" Stationary")
            elif speed < 50:
                print(" City driving")
            else:
                print(" Highway driving")
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n Test stopped by user")
    finally:
        conn.close()
        print(" Connection closed.")
        print(" Mock test completed successfully!")

if __name__ == "__main__":
    main()
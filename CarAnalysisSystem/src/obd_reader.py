import time
import random
import requests

class MockOBDConnection:
    def __init__(self, port=None):
        self.port_name = port or "MOCK_COM_PORT"
        self._connected = True

    def is_connected(self):
        return self._connected

    def query(self, command_type):
        class MockResponse:
            def __init__(self, value):
                self.value = value

        if "RPM" in str(command_type):
            rpm_value = random.randint(800, 3500)
            return MockResponse(type('Q', (), {'magnitude': rpm_value})())

        elif "SPEED" in str(command_type):
            speed_value = random.randint(0, 120)

            class SpeedValue:
                def __init__(self, speed):
                    self.magnitude = speed
                def to(self, unit):
                    return self

            return MockResponse(SpeedValue(speed_value))

        return MockResponse(type('Q', (), {'magnitude': 0})())

    def close(self):
        self._connected = False


def main():
    SERVER_URL = "http://127.0.0.1:5000/add-data"
    conn = MockOBDConnection("COM6")

    print("Connected to:", conn.port_name)

    try:
        while True:
            r_rpm = conn.query("RPM")
            r_speed = conn.query("SPEED")

            rpm = r_rpm.value.magnitude
            speed = r_speed.value.magnitude

            print(f"RPM: {rpm} | Speed: {speed} km/h")

            # 🔥 TRIMITERE CĂTRE WEB
            requests.post(SERVER_URL, json={
                "speed": speed,
                "rpm": rpm
            })

            time.sleep(2)

    except KeyboardInterrupt:
        print("Stopped")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

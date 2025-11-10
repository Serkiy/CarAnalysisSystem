# obd_test.py
import obd
import time


PORT = "COM6"  # sau None pentru autoconnect

def main():
    if PORT:
        print(f"Încerc conectarea la port: {PORT}")
        conn = obd.OBD(PORT, timeout=6)
    else:
        print("Încerc conectare automată (auto detect)...")
        conn = obd.OBD(timeout=5)

    if not conn.is_connected():
        print("Nu s-a putut conecta la adaptorul OBD. Verifică: port, alime=ntare la mașină (ignition ON), împerechere Bluetooth.")
        return

    print("Conectat la:", conn.port_name)

    cmd_rpm = obd.commands.RPM
    cmd_speed = obd.commands.SPEED

    try:
        for i in range(20):
            r_rpm = conn.query(cmd_rpm)
            r_speed = conn.query(cmd_speed)

            rpm = r_rpm.value.magnitude if (r_rpm.value is not None) else None
            speed = None
            if r_speed.value is not None:
                try:
                    speed = r_speed.value.to("km/h").magnitude
                except Exception:
                    speed = r_speed.value.magnitude

            print(f"[{i+1}] RPM: {rpm} | Speed: {speed} km/h")
            time.sleep(1)
    finally:
        conn.close()
        print("Conexiune închisă.")

if __name__ == "__main__":
    main()

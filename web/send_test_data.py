import requests
import random
import time

URL = "http://127.0.0.1:5000/add-data"

while True:
    data = {
        "speed": random.randint(0, 120),
        "rpm": random.randint(800, 4000),
        "temperature": random.randint(70, 110)
    }

    r = requests.post(URL, json=data)
    print("Trimis:", data, r.status_code)

    time.sleep(2)

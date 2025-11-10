# Smart Car Health Monitor

## Description

Smart Car Health Monitor is an intelligent system that monitors the car's status in real time through the *OBD-II* port and provides notifications to the driver if critical values or anomalies are detected. It helps improve safety and prevent malfunctions, with live data visualization via a *web dashboard* or mobile app.

---

## Features

- Read data from the ECU via OBD-II (engine temperature, RPM, battery voltage, vehicle speed, etc.)
- Continuous monitoring of critical parameters
- Real-time alerts and notifications
- Storage of historical data for trend analysis
- Detection of abnormal patterns in vehicle behavior

---

## Components

*Hardware:*
- OBD-II USB/Bluetooth module
- Laptop/phone

*Software:*
- Python 3
- Flask or Django for web dashboard
- SQLite or PostgreSQL for data storage
- Python libraries: pyOBD, requests, pandas, matplotlib (optional for charts)

---

## System Architecture


Car (ECU) --> OBD-II Module --> Raspberry Pi --> Data Processing + Anomaly Detection --> Web Dashboard / Notifications


- *OBD-II Module:* reads data from the car.
- *Program:* central processor, collects and analyzes data.
- *Dashboard:* displays data, trends, and alerts to the driver.

---

## Installation

1. Clone the repository:

bash
git clone https://github.com/username/smart-car-health-monitor.git
cd smart-car-health-monitor


2. Install dependencies:

bash
pip install -r requirements.txt


4. Run the server:

bash
python app.py


5. Access the dashboard at http://<PI_IP>:5000

---

## Contribution

Contributions are welcome! Open an *issue* for bugs or suggestions, and submit *pull requests* for improvements or new features.

---

## License

This project is licensed under the *MIT License*. Standard OBD-II data usage does not require special licenses.

---

## Contact

- Email: sergiu.nvk1315@gmail.com
- GitHub: [Serkiy](https://github.com/Serkiy)

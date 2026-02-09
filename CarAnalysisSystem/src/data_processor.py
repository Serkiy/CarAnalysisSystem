# data_processor.py

def analyze_car_data(rpm, speed, temp):
    """
    Analizează datele brute și returnează o listă de recomandări.
    """
    recomandari = []
    
    # Logică pentru turație (RPM)
    if rpm > 3000:
        recomandari.append("Turație ridicată! Schimbă într-o treaptă superioară pentru a proteja motorul.")
    elif rpm < 1500 and speed > 20:
        recomandari.append("Turație prea mică pentru viteza curentă. Schimbă într-o treaptă inferioară.")
    
    # Logică pentru temperatura motorului (Celsius)
    if temp > 105:
        recomandari.append("ALERTA: Temperatură critică! Oprește motorul și verifică lichidul de răcire.")
    elif 0 < temp < 75:
        recomandari.append("Motorul încă nu a ajuns la temperatura optimă. Evită accelerările bruște.")
        
    # Logică viteză vs turație (Eco-driving)
    if speed > 100 and rpm > 2800:
        recomandari.append("Consum ridicat de combustibil la această turație în regim de autostradă.")

    # Dacă totul este în parametri optimi
    if not recomandari:
        recomandari.append("Stil de condus optim. Motorul funcționează în parametri normali.")
        
    return recomandari
import json, time, random, os
from datetime import datetime

# Path folder untuk data stream (sesuai modul)
OUTPUT_PATH = "stream_data/transportation"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Daftar pilihan data (sesuai modul)
locations = ["Jakarta", "Bandung", "Surabaya"]
vehicles = ["Car", "Motorbike", "Taxi"]
i = 1

print("--- Trip Generator Started ---")

while True:
    # Struktur data JSON (sesuai modul)
    data = {
        "trip_id": f"TRX{i}",
        "vehicle_type": random.choice(vehicles),
        "location": random.choice(locations),
        "distance": random.uniform(1, 20),
        "fare": random.randint(10000, 100000),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Menulis data ke file JSON
    with open(f"{OUTPUT_PATH}/trip_{i}.json", "w") as f:
        json.dump(data, f)
        
    print("Generated Trip:", data)
    
    i += 1
    
    # Jeda waktu (di modul tertulis 3, namun untuk hasil cepat seperti hal 63-64,
    # disarankan menggunakan angka yang lebih kecil agar data cepat menumpuk)
    time.sleep(1)
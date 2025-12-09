"""
script de generare automata imagini constelatii folosind Stellarium
genereaza 150 imagini per constelație cu parametri variaţi

am instalalat Stellarium de aici: https://stellarium.org/ro/

am configurat Stellarium manual inainte:
1. deschide Stellarium
2. F2 → Configuration → Tools → Enable RemoteControl plugin
3. restart Stellarium
4. Stellarium va rula pe http://localhost:8090
"""

import requests
import time
import os
from datetime import datetime, timedelta
import json
from PIL import Image
import io


class StellariumController:
    def __init__(self, host="localhost", port=8090):
        self.base_url = f"http://{host}:{port}/api"
        self.screenshot_dir = "data/stellarium_generated"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def check_connection(self):
        """verifică dacă Stellarium este pornit si RemoteControl activ"""
        try:
            response = requests.get(f"{self.base_url}/main/status", timeout=2)
            if response.status_code == 200:
                print(" Conectat la Stellarium!")
                return True
        except:
            print("   Stellarium nu raspunde")
            print("   Pași:")
            print("   1. deschide Stellarium")
            print("   2. F2 → Configuration → Plugins → RemoteControl → Enable")
            print("   3. Restart Stellarium")
            return False

    def set_location(self, lat, lon, altitude=100, name="Custom"):
        """seteaza locatia geografica"""
        data = {
            "latitude": lat,
            "longitude": lon,
            "altitude": altitude,
            "name": name
        }
        response = requests.post(f"{self.base_url}/location/setlocationfields", json=data)
        return response.status_code == 200

    def set_time(self, year, month, day, hour, minute=0):
        """seteaza data si ora"""
        # format: "2024-12-06T22:30:00"
        time_str = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00"
        response = requests.post(
            f"{self.base_url}/main/time",
            data={"time": time_str, "timerate": 0}
        )
        return response.status_code == 200

    def find_constellation(self, constellation_name):
        """cauta si centreaza pe constelatie"""
        # nume acceptate: "ursa minor", "ursa major", "pegasus", "andromeda"
        response = requests.post(
            f"{self.base_url}/main/focus",
            data={"target": constellation_name}
        )
        time.sleep(0.5)  # așteapta sa se centreze
        return response.status_code == 200

    def set_fov(self, fov_degrees):
        """seteaza campul vizual"""
        response = requests.post(
            f"{self.base_url}/main/fov",
            data={"fov": fov_degrees}
        )
        return response.status_code == 200

    def set_view_direction(self, azimuth, altitude):
        """seteaza directia de vizualizare
        azimuth: 0-360° (0=nord, 90=est, 180=sud, 270=vest)
        altitude: 0-90° (0=orizont, 90=zenit)
        """
        response = requests.post(
            f"{self.base_url}/main/view",
            json={"azimuth": azimuth, "altitude": altitude}
        )
        return response.status_code == 200

    def toggle_constellation_lines(self, show=True):
        """activeaza/dezactiveaza liniile constelatiilor"""
        action = "on" if show else "off"
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Constellation_Lines"})

    def toggle_constellation_labels(self, show=True):
        """activeaza/dezactiveaza etichetele constelatiilor"""
        action = "on" if show else "off"
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Constellation_Labels"})

    def toggle_atmosphere(self, show=False):
        """activeaza/dezactiveaza atmosfera (pentru cer mai negru)"""
        requests.post(f"{self.base_url}/stelaction/do", data={"id": "actionShow_Atmosphere"})

    def take_screenshot(self, filename):
        """face screenshot si salveaza"""
        # Stellarium salveaza automat în folder-ul de screenshots
        requests.post(f"{self.base_url}/main/screenshot")
        time.sleep(0.5)
        print(f"   Screenshot salvat (Stellarium folder)")
        return True

    def save_view_info(self, filename, metadata):
        """salveaza metadata despre imagine"""
        json_file = filename.replace('.png', '.json')
        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=2)


def generate_constellation_dataset(constellation_name, num_images=100):
    """
    generează dataset complet pentru o constelație

    Args:
        constellation_name: "ursa minor", "ursa major", "pegasus", "andromeda"
        num_images: numar de imagini de generat
    """

    controller = StellariumController()

    # verifica conexiunea
    if not controller.check_connection():
        return

    print(f"\n Generam {num_images} imagini pentru {constellation_name}...")

    # configurare initiala
    controller.toggle_constellation_lines(False)  # fara linii
    controller.toggle_constellation_labels(False)  # fara etichete
    controller.toggle_atmosphere(False)  # fara atmosfera

    # parametri de variație
    locations = [
        (44.4268, 26.1025, "Bucuresti"),
        (45.6580, 25.6012, "Brasov"),
        (47.1585, 27.6014, "Iasi"),
        (46.7712, 23.6236, "Cluj-Napoca"),
        (45.9432, 24.9668, "Sibiu"),
        (44.1598, 28.6348, "Constanta"),
    ]

    months = range(1, 13)  # ianuarie - decembrie
    hours = [20, 21, 22, 23, 0, 1, 2, 3, 4]  # 20:00 - 04:00
    fovs = [30, 40, 50, 60, 70]  # field of view in grade

    output_dir = f"data/stellarium_generated/{constellation_name.lower().replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)

    img_count = 0

    # genereaza imagini cu combinatii diferite
    for loc_idx, (lat, lon, loc_name) in enumerate(locations):
        if img_count >= num_images:
            break

        controller.set_location(lat, lon, name=loc_name)
        print(f"\ Locatie: {loc_name} ({lat}°, {lon}°)")

        for month in months:
            if img_count >= num_images:
                break

            for hour in hours:
                if img_count >= num_images:
                    break

                # seteaza timpul
                controller.set_time(2024, month, 15, hour)

                # cauta constelatia
                if controller.find_constellation(constellation_name):

                    # variaza FOV-ul
                    for fov in fovs:
                        if img_count >= num_images:
                            break

                        controller.set_fov(fov)
                        time.sleep(0.3)  # asteapta render

                        # salveaza screenshot
                        filename = f"{constellation_name.lower().replace(' ', '_')}_{img_count:04d}.png"
                        filepath = os.path.join(output_dir, filename)

                        metadata = {
                            "constellation": constellation_name,
                            "location": loc_name,
                            "latitude": lat,
                            "longitude": lon,
                            "date": f"2024-{month:02d}-15",
                            "hour": hour,
                            "fov": fov,
                            "image_id": img_count
                        }

                        controller.take_screenshot(filepath)
                        controller.save_view_info(filepath, metadata)

                        img_count += 1
                        print(f" {img_count}/{num_images} - {filename}")

                        time.sleep(0.2)  # pauza mica intre screenshots

    print(f"\n Am generat {img_count} imagini pentru {constellation_name}!")
    print(f"📁 Salvate in: {output_dir}")
    return output_dir


def generate_full_dataset():
    """genereaza dataset complet pentru toate cele 4 constelatii"""

    constellations = {
        "Ursa Minor": 150,  # 150 imagini
        "Ursa Major": 150,  # 150 imagini
        "Pegasus": 150,  # 150 imagini
        "Andromeda": 150  # 150 imagini
    }

    print("=" * 60)
    print(" generator automat dataset constelatii")
    print("=" * 60)
    print("\n plan:")
    for const, num in constellations.items():
        print(f"   • {const}: {num} imagini")
    print(f"\n total: {sum(constellations.values())} imagini")
    print("  timp estimat: ~15-30 minute")
    print("\n asigura-te ca Stellarium este deschis si RemoteControl activ!")
    input("\napasa enter pentru a incepe...")

    start_time = time.time()

    for constellation, num_images in constellations.items():
        print("\n" + "=" * 60)
        output_dir = generate_constellation_dataset(constellation, num_images)
        print(f" {constellation} - complet")
        print("=" * 60)
        time.sleep(2)  # pauza intre constelatii

    elapsed = time.time() - start_time
    print(f"\n DATASET COMPLET GENERAT!")
    print(f"️  timp total: {elapsed / 60:.1f} minute")
    print(f" locație: data/stellarium_generated/")

    # statistici
    print("\n statistici:")
    total_images = 0
    for const in constellations.keys():
        folder = f"data/stellarium_generated/{const.lower().replace(' ', '_')}"
        if os.path.exists(folder):
            count = len([f for f in os.listdir(folder) if f.endswith('.png')])
            total_images += count
            print(f"   • {const}: {count} imagini")
    print(f"\n   total: {total_images} imagini ")

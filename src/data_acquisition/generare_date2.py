"""
SCRIPT STABIL - Generare automata imagini constelatii (JPEG, 500x500)
Folosește metoda de mutare a fișierelor generice 'stellarium-xxxx.jpeg'
pentru a evita eroarea HTTP 400 la setarea căii.
"""

import requests
import time
import os
import sys
import warnings
import json
import shutil # Pentru mutarea fișierelor
from glob import glob # Pentru căutarea fișierelor
import requests.exceptions
from urllib3.exceptions import NotOpenSSLWarning

# Suprimă avertizarea NotOpenSSLWarning/LibreSSL
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


class StellariumController:
    def __init__(self, host="localhost", port=8090):
        self.base_url = f"http://{host}:{port}/api"

        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.target_dir_root = os.path.join(self.project_root, "data", "generated")
        os.makedirs(self.target_dir_root, exist_ok=True)

        # Calea unde Stellarium SALVEAZĂ (SETATĂ MANUAL în F2, ex: /tmp)
        self.stellarium_save_dir = "/tmp"

        print(f"   Directorul FINAL al Proiectului (JPEG & JSON): {self.target_dir_root}")
        print(f"   Directorul de Căutare (Setare Stellarium): {self.stellarium_save_dir}")


    def check_connection(self):
        """verifică dacă Stellarium este pornit si RemoteControl activ"""
        # (Funcția de verificare conexiune rămâne la fel)
        try:
            print(f"\n   Încercare conexiune la: {self.base_url}/main/status (timeout 5s)")
            response = requests.get(f"{self.base_url}/main/status", timeout=5)

            if response.status_code == 200:
                print(" Conectat la Stellarium!")
                return True
            else:
                print(f"   Stellarium a răspuns, dar cu codul HTTP: {response.status_code}")
                return False

        except requests.exceptions.ConnectionError:
            print("   Stellarium nu răspunde (Eroare de Conexiune).")
            return False

        except Exception as e:
            print(f"   Eroare neașteptată la conectare: {e}")
            return False

    # --- Funcții de Vedere (la fel ca înainte) ---
    def set_location(self, lat, lon, altitude=100, name="Custom"):
        data = {"latitude": lat, "longitude": lon, "altitude": altitude, "name": name}
        response = requests.post(f"{self.base_url}/location/setlocationfields", json=data)
        return response.status_code == 200

    def set_time(self, year, month, day, hour, minute=0):
        time_str = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00"
        response = requests.post(f"{self.base_url}/main/time", data={"time": time_str, "timerate": 0})
        return response.status_code == 200

    def find_constellation(self, constellation_name):
        response = requests.post(f"{self.base_url}/main/focus", data={"target": constellation_name})
        time.sleep(0.5)
        return response.status_code == 200

    def set_fov(self, fov_degrees):
        response = requests.post(f"{self.base_url}/main/fov", data={"fov": fov_degrees})
        return response.status_code == 200

    def toggle_clean_view(self):
        """Dezactivează toate elementele de interfață."""
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Constellation_Lines"})
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Constellation_Labels"})
        requests.post(f"{self.base_url}/stelaction/do", data={"id": "actionShow_Atmosphere"})
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Star_Names"})
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Planet_Labels"})
        requests.post(f"{self.base_url}/stelaction/do", data={"id": f"actionShow_Ecliptic_J2000_Grid"})

    # --- Funcții de Salvare ---

    def take_screenshot(self):
        """Trimite comanda de screenshot simplă."""
        requests.post(f"{self.base_url}/main/screenshot")
        return True

    def move_last_screenshot(self, target_path, timeout=5):
        """Caută cel mai nou fișier 'stellarium-xxxx.jpeg' în directorul temporar și îl mută/redenumește."""

        start_time = time.time()
        # Căutăm fișierul generic pe care Stellarium îl generează
        search_path = os.path.join(self.stellarium_save_dir, "stellarium-*.jpeg")

        while time.time() - start_time < timeout:
            # Găsește toate fișierele .jpeg care încep cu 'stellarium-'
            list_of_files = glob(search_path)

            if list_of_files:
                # Găsește cel mai nou fișier pe baza timpului de modificare
                latest_file = max(list_of_files, key=os.path.getmtime)

                # Mută fișierul temporar în calea finală
                try:
                    shutil.move(latest_file, target_path)
                    return True
                except Exception as e:
                    print(f"   ✗ Eroare la mutarea fișierului {latest_file}: {e}")
                    return False

            time.sleep(0.1)

        print(f"   ✗ Stellarium nu a salvat imaginea (sau fișierul nu a apărut în {self.stellarium_save_dir})")
        return False


    def save_view_info(self, filename, metadata):
        """salveaza metadata (.json) alături de imaginea (.jpeg)."""
        json_file = filename.replace('.jpeg', '.json')
        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=2)


def generate_constellation_dataset(constellation_name, num_images=100, controller=None):
    """generează dataset complet pentru o constelație"""

    if not controller.check_connection():
        print(f"\nGenerare anulată pentru {constellation_name} din cauza eșecului de conectare.")
        return

    print(f"\n Generăm {num_images} imagini pentru {constellation_name}...")

    controller.toggle_clean_view()

    # parametri de variație (la fel ca înainte)
    locations = [
        (44.4268, 26.1025, "Bucuresti"), (45.6580, 25.6012, "Brasov"), (47.1585, 27.6014, "Iasi"),
        (46.7712, 23.6236, "Cluj-Napoca"), (45.9432, 24.9668, "Sibiu"), (44.1598, 28.6348, "Constanta"),
    ]
    months = range(1, 13)
    hours = [20, 21, 22, 23, 0, 1, 2, 3, 4]
    fovs = [30, 40, 50, 60, 70]

    constellation_folder = constellation_name.lower().replace(' ', '_')
    output_dir = os.path.join(controller.target_dir_root, constellation_folder)
    os.makedirs(output_dir, exist_ok=True)

    img_count = 0

    for loc_idx, (lat, lon, loc_name) in enumerate(locations):
        if img_count >= num_images: break

        controller.set_location(lat, lon, name=loc_name)
        print(f"\n Locație: {loc_name} ({lat}°, {lon}°)")

        for month in months:
            if img_count >= num_images: break
            for hour in hours:
                if img_count >= num_images: break

                controller.set_time(2024, month, 15, hour)
                if controller.find_constellation(constellation_name):
                    for fov in fovs:
                        if img_count >= num_images: break

                        controller.set_fov(fov)
                        time.sleep(0.3)

                        filename = f"{constellation_folder}_{img_count:04d}.jpeg"
                        target_filepath = os.path.join(output_dir, filename)

                        # 1. Trimite comanda de screenshot
                        controller.take_screenshot()

                        # 2. Caută, mută și redenumește fișierul generic 'stellarium-xxxx.jpeg'
                        if controller.move_last_screenshot(target_filepath):
                            # 3. Salvează metadatele
                            metadata = {
                                "constellation": constellation_name, "location": loc_name, "latitude": lat,
                                "longitude": lon, "date": f"2024-{month:02d}-15", "hour": hour,
                                "fov": fov, "image_id": img_count, "image_filename": filename
                            }
                            controller.save_view_info(target_filepath, metadata)

                            img_count += 1
                            print(f" {img_count}/{num_images} - {filename} salvat.")

                        time.sleep(0.2)

    print(f"\n Am generat {img_count} seturi (.json și .jpeg) pentru {constellation_name}!")
    return output_dir


def generate_full_dataset():
    """genereaza dataset complet pentru toate cele 4 constelatii"""

    print("\n>>> DATASET GENERATOR INCEPE EXECUTIA...", file=sys.stderr)

    controller = StellariumController()

    print("\n--- VERIFICĂRI ESSENȚIALE ---")
    print("1. Stellarium (F2) 'Screenshot Directory' este setat la calea simplă: ** /tmp/ **?")
    print("2. 'File format' este **.jpeg** și 'Custom size' este **500 x 500**?")
    print(f"3. Directorul de salvare este: {controller.target_dir_root}")
    print("----------------------------")

    constellations = {"Ursa Minor": 150, "Ursa Major": 150, "Pegasus": 150, "Andromeda": 150 }

    print("=" * 60)
    print(" generator automat dataset constelatii")
    print("=" * 60)
    print(f"\n total: {sum(constellations.values())} imagini")
    input("\napasa enter pentru a începe...")

    start_time = time.time()

    for constellation, num_images in constellations.items():
        print("\n" + "=" * 60)
        output_dir = generate_constellation_dataset(constellation, num_images, controller=controller)
        print(f" {constellation} - complet")
        print("=" * 60)
        time.sleep(2)

    elapsed = time.time() - start_time
    print(f"\n DATASET COMPLET GENERAT!")
    print(f"️  timp total: {elapsed / 60:.1f} minute")
    print(f" locație fișiere: {controller.target_dir_root}")

    # statistici finale
    print("\n statistici:")
    total_files = 0
    for const in constellations.keys():
        folder = os.path.join(controller.target_dir_root, const.lower().replace(' ', '_'))
        if os.path.exists(folder):
            count_json = len([f for f in os.listdir(folder) if f.endswith('.json')])
            count_jpeg = len([f for f in os.listdir(folder) if f.endswith('.jpeg')])
            total_files += count_json
            print(f"   • {const}: {count_json} fișiere .json și {count_jpeg} fișiere .jpeg")
    print(f"\n   total: {total_files} seturi de fișiere (JSON și JPEG) ")

if __name__ == "__main__":
    generate_full_dataset()
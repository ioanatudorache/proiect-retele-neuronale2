import os
import cv2
import numpy as np
from pathlib import Path
import random


class ConstellationAugmenter:
    def __init__(self, input_dir, output_dir, target_count=1000):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.target_count = target_count

    def rotate_image(self, image, angle):
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height),
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(0, 0, 0))
        return rotated

    def flip_image(self, image, mode):
        return cv2.flip(image, mode)

    def adjust_brightness(self, image, factor):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 2] = hsv[:, :, 2] * factor
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    def adjust_contrast(self, image, factor):
        mean = np.mean(image)
        adjusted = (image - mean) * factor + mean
        return np.clip(adjusted, 0, 255).astype(np.uint8)

    def add_noise(self, image, noise_level):
        noise = np.random.normal(0, noise_level, image.shape)
        noisy_image = image.astype(np.float32) + noise
        return np.clip(noisy_image, 0, 255).astype(np.uint8)

    def translate_image(self, image, tx, ty):
        height, width = image.shape[:2]
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        translated = cv2.warpAffine(image, translation_matrix, (width, height),
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(0, 0, 0))
        return translated

    def zoom_image(self, image, zoom_factor):
        height, width = image.shape[:2]
        new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

        #redimensioneaza
        resized = cv2.resize(image, (new_width, new_height))

        if zoom_factor > 1:  #zoom in - crop center
            start_y = (new_height - height) // 2
            start_x = (new_width - width) // 2
            return resized[start_y:start_y + height, start_x:start_x + width]
        else:  #zoom out - add padding
            result = np.zeros((height, width, 3), dtype=np.uint8)
            start_y = (height - new_height) // 2
            start_x = (width - new_width) // 2
            result[start_y:start_y + new_height, start_x:start_x + new_width] = resized
            return result

    def apply_blur(self, image, kernel_size):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def augment_image(self, image, augmentation_params):
        augmented = image.copy()

        # rotație
        if 'rotation' in augmentation_params:
            augmented = self.rotate_image(augmented, augmentation_params['rotation'])

        # flip
        if 'flip' in augmentation_params:
            augmented = self.flip_image(augmented, augmentation_params['flip'])

        # brightness
        if 'brightness' in augmentation_params:
            augmented = self.adjust_brightness(augmented, augmentation_params['brightness'])

        # contrast
        if 'contrast' in augmentation_params:
            augmented = self.adjust_contrast(augmented, augmentation_params['contrast'])

        # noise
        if 'noise' in augmentation_params:
            augmented = self.add_noise(augmented, augmentation_params['noise'])

        # translation
        if 'translation' in augmentation_params:
            tx, ty = augmentation_params['translation']
            augmented = self.translate_image(augmented, tx, ty)

        # zoom
        if 'zoom' in augmentation_params:
            augmented = self.zoom_image(augmented, augmentation_params['zoom'])

        # blur
        if 'blur' in augmentation_params:
            augmented = self.apply_blur(augmented, augmentation_params['blur'])

        return augmented

    def generate_random_params(self):
        params = {}

        # probabilitate de aplicare pentru fiecare augmentare
        if random.random() > 0.3:
            params['rotation'] = random.uniform(-180, 180)

        if random.random() > 0.5:
            params['flip'] = random.choice([0, 1, -1])

        if random.random() > 0.4:
            params['brightness'] = random.uniform(0.6, 1.4)

        if random.random() > 0.4:
            params['contrast'] = random.uniform(0.7, 1.3)

        if random.random() > 0.5:
            params['noise'] = random.uniform(2, 15)

        if random.random() > 0.5:
            tx = random.randint(-30, 30)
            ty = random.randint(-30, 30)
            params['translation'] = (tx, ty)

        if random.random() > 0.5:
            params['zoom'] = random.uniform(0.8, 1.2)

        if random.random() > 0.7:
            kernel_size = random.choice([3, 5])
            params['blur'] = kernel_size

        return params

    def process_constellation(self, image_path, constellation_name):
        #procesează o singura imagine de constelatie si genereaza augmentari
        print(f"\nProcesare: {constellation_name}")

        # citește imaginea
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # creează director de output
        output_constellation_dir = self.output_dir / constellation_name
        output_constellation_dir.mkdir(parents=True, exist_ok=True)

        # salvează imaginea originală
        original_path = output_constellation_dir / f"{constellation_name}_original.jpg"
        cv2.imwrite(str(original_path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        print(f"  Salvată imaginea originală")

        # generează imagini augmentate
        for i in range(self.target_count - 1):  # -1 pentru că am salvat deja originalul
            # generează parametri aleatori
            params = self.generate_random_params()

            # aplică augmentări
            augmented = self.augment_image(image, params)

            # Salvează imaginea augmentată
            output_path = output_constellation_dir / f"{constellation_name}_aug_{i + 1:04d}.jpg"
            cv2.imwrite(str(output_path), cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))

            # Progress bar
            if (i + 1) % 100 == 0:
                print(f"  Progres: {i + 1}/{self.target_count - 1} imagini generate")

        print(f"✓ Finalizat {constellation_name}: {self.target_count} imagini totale")

    def process_all(self):
        # găsește toate imaginile jpg
        image_files = list(self.input_dir.glob("*.jpg"))

        if len(image_files) == 0:
            print(f"EROARE: Nu s-au găsit imagini jpg în {self.input_dir}")
            return

        print(f"Găsite {len(image_files)} imagini pentru augmentare")
        print(f"Target: {self.target_count} imagini pentru fiecare constelație")
        print(f"Total imagini ce vor fi generate: {len(image_files) * self.target_count}")
        print("=" * 60)

        # procesează fiecare imagine
        for image_path in image_files:
            constellation_name = image_path.stem  # numele fișierului fără extensie
            self.process_constellation(image_path, constellation_name)

        print("\n" + "=" * 60)
        print(f"Toate imaginile au fost augmentate.")
        print(f" Rezultate salvate în: {self.output_dir}")


def main():

    # configurare
    INPUT_DIR = "../../data/raw/input"  # director cu cele 4 imagini originale
    OUTPUT_DIR = "../../data/processed/output"  # director unde se salvează rezultatele
    TARGET_COUNT = 1000  # cate imagini vrem pentru fiecare constelație

    # creează augmenter
    augmenter = ConstellationAugmenter(
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        target_count=TARGET_COUNT
    )

    # procesează toate imaginile
    augmenter.process_all()


if __name__ == "__main__":
    main()
import os
import shutil
import random

source_root = "/Users/ioanatudorache/Documents/GitHub/proiect-retele-neuronale/data/processed/output"
train_root = "/Users/ioanatudorache/Documents/GitHub/proiect-retele-neuronale/data/processed/train"
test_root = "/Users/ioanatudorache/Documents/GitHub/proiect-retele-neuronale/data/processed/test"
val_root = "/Users/ioanatudorache/Documents/GitHub/proiect-retele-neuronale/data/processed/validation"

for cls in os.listdir(source_root):
    class_path = os.path.join(source_root, cls)

    if not os.path.isdir(class_path):
        continue

    clean_cls = cls.replace("-2", "")

    train_dir = os.path.join(train_root, clean_cls)
    test_dir = os.path.join(test_root, clean_cls)
    val_dir = os.path.join(val_root, clean_cls)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    images = os.listdir(class_path)
    random.shuffle(images)

    total = len(images)
    train_count = int(0.8 * total)
    test_count = int(0.1 * total)
    val_count = total - train_count - test_count

    train_images = images[:train_count]
    test_images = images[train_count:train_count+test_count]
    val_images = images[train_count+test_count:]

    def move_images(img_list, target_folder):
        for img in img_list:
            shutil.move(
                os.path.join(class_path, img),
                os.path.join(target_folder, img)
            )

    move_images(train_images, train_dir)
    move_images(test_images, test_dir)
    move_images(val_images, val_dir)

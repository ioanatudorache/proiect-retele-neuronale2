import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os


# 1. definim arhitectura
def defineste_model_constelatii():
    """
        Arhitectura de Retea Neuronala Convolutionala (CNN) pentru clasificare a 4 constelatii.

        Justificare pentru Arhitectura Aleasa:
        1.  *Conv2D/MaxPooling2D:* CNN-urile sunt arhitectura standard pentru clasificarea
            imaginilor. Straturile Conv2D extrag automat caracteristici ierarhice (margini,
            forme) din imagini, iar MaxPooling2D reduce dimensiunea spațială, minimizand
            complexitatea și numărul de parametri, prevenind supra-antrenarea.
        2.  *Flatten:* Schimba output-ul pooling layerelor intr-un vector 1D pentru ca layerele Dense
            asteapta un input 1D ca sa faca clasificarea finala a imaginilor.
        3.  *Dense:* Straturile fully-connected (dense) realizeaza clasificarea efectiva
            pe baza caracteristicilor extrase.
        4.  *Dropout:* Stratul de Dropout (rată de 0.5) este inclus pentru a reduce
            supra-antrenarea, prin oprirea aleatorie a 50% din neuroni in timpul
            antrenarii.
        5.  *Stratul de Iesire (Dense):* Are 4 unitati (egal cu numarul de clase) și foloseste
            funcția de activare 'softmax' pentru a produce o distributie de probabilitate
            pentru cele 4 clase, indicand probabilitatea ca imaginea sa apartina
            fiecarei clase.
        """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(4, activation='softmax')
    ])
    return model


# 2. configuram caile
base_path = "/Users/ioanatudorache/Documents/GitHub/proiect-retele-neuronale"
models_dir = os.path.join(base_path, "models")
file_path = os.path.join(models_dir, "untrained_model.h5")

# 3. executam si salvam codul
if __name__ == "__main__":
    print("--- Pornire script model ---")

    # cream modelul
    model_final = defineste_model_constelatii()

    # ne asiguram ca folderul exista fizic
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Creat folderul: {models_dir}")

    # stergem fisierul vechi daca exista (ca sa fim siguri ca cel nou e fresh)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Am șters fișierul vechi de 0 bytes.")

    # salvam
    print(f"Se salvează modelul la: {file_path} ...")
    model_final.save(file_path)

    # 4. verificare finala
    if os.path.exists(file_path):
        dimensiune = os.path.getsize(file_path)
        if dimensiune > 1000:  # un model de 26MB are peste 1000 bytes
            print(f"Locatie: {file_path}")
            print(f"Dimensiune: {dimensiune / (1024 * 1024):.2f} MB")
        else:
            print(f"Fisierul a fost creat dar are doar {dimensiune} bytes.")
    else:
        print(" Fișierul nu a putut fi creat deloc.")
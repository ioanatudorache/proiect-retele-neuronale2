import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

# definim parametrii necesari
NUM_CLASE = 4  # andromeda, ursa major, ursa minor, pegasus
DIMENSIUNE_IMAGINE = (500, 500)  # dimensiune standard a fiecaror imagini
CANALE_CULOARE = 3  # RGB

def defineste_model_constelatii():
    """
    Arhitectura de Rețea Neuronala Convoluționala (CNN) pentru clasificare a 4 constelații.

    Justificare pentru Arhitectura Aleasa:
    1.  **Conv2D/MaxPooling2D:** CNN-urile sunt arhitectura standard pentru clasificarea
        imaginilor. Straturile Conv2D extrag automat caracteristici ierarhice (margini,
        forme) din imagini, iar MaxPooling2D reduce dimensiunea spațială, diminuând
        complexitatea și numărul de parametri, prevenind supra-antrenarea.
    2.  **Flatten:** Converteste harta de caracteristici 2D (ieșirea CNN) într-un
        vector 1D necesar pentru straturile Dense (fully-connected).
    3.  **Dense:** Straturile fully-connected (dense) realizează clasificarea efectivă
        pe baza caracteristicilor extrase.
    4.  **Dropout:** Stratul de Dropout (rată de 0.5) este inclus pentru a reduce
        supra-antrenarea, prin "întreruperea" aleatorie a 50% din neuroni în timpul
        antrenării.
    5.  **Stratul de Ieșire (Dense):** Are 4 unități (egal cu NUM_CLASE) și folosește
        funcția de activare **'softmax'** pentru a produce o distribuție de probabilitate
        pentru cele 4 clase (constelații), indicând probabilitatea ca imaginea să aparțină
        fiecărei clase.
    """
    model = Sequential([
        # bloc 1
        Conv2D(32, (3, 3), activation='relu', input_shape=(DIMENSIUNE_IMAGINE[0], DIMENSIUNE_IMAGINE[1], CANALE_CULOARE)),
        MaxPooling2D((2, 2)),

        # bloc 2
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        # bloc 3
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Flatten(),

        # straturi dense (Fully Connected)
        Dense(512, activation='relu'),
        Dropout(0.5),

        # stratul de ieșire
        Dense(NUM_CLASE, activation='softmax')
    ])
    return model

model = defineste_model_constelatii()
model.summary()
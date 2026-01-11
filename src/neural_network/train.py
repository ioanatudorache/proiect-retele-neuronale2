import tensorflow as tf
from model import defineste_model_constelatii #modelul din etapa 4
import pandas as pd

# 1. incarcam datele
train_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory( #normalizam valorile
    'data/train', target_size=(128, 128), batch_size=32, class_mode='categorical') #redimensionam imaginile la 128x128 si
      #antrenam modelul in mini batch uri de 32

val_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(
    'data/validation', target_size=(128, 128), batch_size=32, class_mode='categorical')

# 2. configuram modelul
model = defineste_model_constelatii()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 3. antrenam, am ales 15 epoci
history = model.fit(train_gen, validation_data=val_gen, epochs=15)

# 4. salvam modelul
model.save('models/trained_model.h5') # Fișierul cheie
pd.DataFrame(history.history).to_csv('results/training_history.csv', index=False) # istoric
print("Modelul s-a antrenat și s-a salvat.")
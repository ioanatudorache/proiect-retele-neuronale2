import tensorflow as tf
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# 1. incarcam modelul si datele de test
model = tf.keras.models.load_model('models/trained_model.h5')

# presupunem ca folosim un generator pentru test_set
test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    'data/test',
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    shuffle=False  # pentru Confusion Matrix
)

# 2. predictii
predictions = model.predict(test_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

# 3. calcul metrici
report = classification_report(y_true, y_pred, target_names=class_labels, output_dict=True)
f1_macro = f1_score(y_true, y_pred, average='macro')
accuracy = report['accuracy']

# salvam metrici in json
metrics = {
    "test_accuracy": accuracy,
    "test_f1_macro": f1_macro,
    "classes": report
}

with open('results/test_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

# 4. generare Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_labels, yticklabels=class_labels, cmap='Blues')
plt.xlabel('Predictie')
plt.ylabel('Adevar (Ground Truth)')
plt.title('Confusion Matrix - Clasificare Constelatii')
plt.savefig('docs/confusion_matrix.png')
plt.show()

print(f"Am terminat evaluarea! Accuracy: {accuracy:.2f}, F1: {f1_macro:.2f}")
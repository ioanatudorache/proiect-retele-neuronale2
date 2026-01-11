from tkinter import Image

import streamlit as st
import pandas as pd
import numpy as np

from src.neural_network.evaluate import model
from datetime import datetime

if 'istoric_cautari' not in st.session_state:
    st.session_state.istoric_cautari = []

st.title("Clasificarea Constelatiilor")
st.write("Incarca o imagine cu cerul pentru a identifica constelatia")

# dictionar cu informatii despre fiecare constelatie
info_constelatii = {
    "Andromeda": {
        "descriere": "Cunoscuta pentru Galaxia Andromeda (M31), cel mai apropiat vecin mare al Caii Lactee.",
        "vizibilitate": "Cel mai bine vizibila toamna in emisfera nordica.",
        "curiozitate": "Se afla la aproximativ 2.5 milioane de ani-lumina distanta de noi.",
        "nume" : "Andromeda e fata Cassiopeei si sotia eroului Perseu."
    },
    "Ursa Major": {
        "descriere": "Contine faimosul grup de stele 'Carul Mare'.",
        "vizibilitate": "Vizibila tot anul din majoritatea locurilor din emisfera nordica.",
        "curiozitate": "Stelele sale sunt folosite pentru a gasi Steaua Polara.",
        "nume" : "In latina inseamna ursul mare. Zeus se indragosteste de Callisto, una dintre nimfele lui Artemis, iar sotia lui, Hera, afla. Aceasta o transforma pe Callisto intr-o ursoaica drept pedeapsa."
    },
    "Ursa Minor": {
        "descriere": "Gazduieste Steaua Polara (Polaris), punctul de reper pentru nord.",
        "vizibilitate": "Vizibila pe tot parcursul anului in emisfera nordica.",
        "curiozitate": "Este mult mai greu de vazut decât Ursa Major din cauza stelelor mai slabe.",
        "nume" : "Zeus l-a transformat pe fiul lui Callisto, Arcas, intr-un urs mic ca sa il salveze de Hera."
    },
    "Pegasus": {
        "descriere": "Recunoscuta după 'Marele Patrat', reprezinta calul inaripat din mitologie.",
        "vizibilitate": "Se vede cel mai bine la sfarsitul verii si toamna.",
        "curiozitate": "Aici a fost descoperita prima planeta din afara sistemului nostru solar (51 Pegasi b).",
        "nume" : "Pegasus provine de la animalul mitologic grecesc, nascut din sangele Meduzei. Acesta a fost calul inaripat a lui Zeus, aducandu-i fulgere."
    }
}

@st.cache_resource
def load_my_model ():
    return model.load_model('models/untrained_model.h5')
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    else:
        st.error("Modelul antrenat nu a putut fi gasit")
        return None
modal = load_my_model()

uploded_file = st.file.uploader("Alege o imagine...", type=["jpeg", "jpg", "png"])

if uploded_file is not None:
    image = Image.open(uploded_file) #afisam imaginea uploadata
    st.image(image, caption="Imagine incarcata", use_column_width=True)

    st.write("Se analizeaza...")

    img = image.resize((128, 128)) #redimensionam imaginea la 128x128
    img = np.array(img) / 255.0 #convertim la array si normalizam
    img_array = np.expand_dims(img, axis=0) #adaugam dimensiunea batch

if model:
    predictions = model.predict(img_array)
    clase = ['Andromeda', 'Pegasus', 'Ursa Minor', 'Ursa Major']
    rezultat = clase[np.argmax(predictions)]
    probabilitate = np.max(predictions) * 100

st.success(f"Constelatia detectata: **{rezultat}**")
st.info(f"Probabilitate: {probabilitate:.2f}%")

if model:
    predictions = model.predict(img_array)
    clase = ['Andromeda', 'Pegasus', 'Ursa Major', 'Ursa Minor']
    rezultat = clase[np.argmax(predictions)]

    st.success(f"Constelația detectată: **{rezultat}**")

    ora_actuala = datetime.now().strftime("%H:%M:%S")
    st.session_state.istoric_cautari.insert(0, f"[{ora_actuala}] {rezultat}")

    # sectiunea de informatii
    if rezultat in info_constelatii:
        date = info_constelatii[rezultat]

        st.subheader(f"Despre {rezultat}")

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Descriere:** \n{date['descriere']}")
        with col2:
            st.warning(f"**Cand o poti vedea:** \n{date['vizibilitate']}")

        with st.expander("Stiai ca...?"):
            st.write(date['curiozitate'])

with st.sidebar:
    st.header("Istoric cautari")

    if not st.session_state.istoric_cautari:
        st.write("Nicio cautare efectuata inca.")
    else:
        if st.button("Sterge istoricul"):
            st.session_state.istoric_cautari = []
            st.rerun()

            for item in st.session_state.istoric_cautari[:15]:
                st.write(item)
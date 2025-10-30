import streamlit as st
import os
import time
import glob
import urllib.request
from gtts import gTTS
from PIL import Image
import base64

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Fábula Sonora", page_icon="🎧", layout="centered")

# --- TÍTULO Y ESTILO ---
st.markdown(
    """
    <h1 style='text-align: center; color: #2e86de;'>🎧 Conversión de Texto a Audio</h1>
    <p style='text-align: center; color: #6c757d;'>Convierte tus palabras en voz y escucha cómo cobran vida.</p>
    """,
    unsafe_allow_html=True,
)

# --- IMAGEN: The Thinker ---
image_url = "https://upload.wikimedia.org/wikipedia/commons/1/12/The_Thinker%2C_Rodin.jpg"
req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    img = Image.open(response)
st.image(img, width=350, caption="The Thinker — Auguste Rodin")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🗒️ Instrucciones")
    st.write("1️⃣ Escribe o copia un texto que quieras escuchar.")
    st.write("2️⃣ Selecciona el idioma.")
    st.write("3️⃣ Pulsa **Convertir a Audio**.")
    st.info("Tu archivo se descargará automáticamente cuando esté listo.")

# --- CARPETA TEMPORAL ---
os.makedirs("temp", exist_ok=True)

# --- FÁBULA DE EJEMPLO ---
st.subheader("Una pequeña Fábula 🐭🐱")
st.write(
    "¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. "
    "Al principio era tan grande que le tenía miedo. Corría y corría y, por cierto, "
    "me alegraba ver esos muros, a diestra y siniestra, en la distancia. "
    "Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto "
    "y ahí, en el rincón, está la trampa sobre la cual debo pasar. "
    "‘Todo lo que debes hacer es cambiar de rumbo’, dijo el gato... y se lo comió. — Franz Kafka."
)

# --- ENTRADA DE TEXTO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📝 Ingresa el texto que deseas convertir a voz:")
text = st.text_area("Escribe o pega tu texto aquí:", "")

# --- SELECCIÓN DE IDIOMA ---
option_lang = st.selectbox("🌐 Selecciona el idioma", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

# --- FUNCIÓN PRINCIPAL: TEXT TO SPEECH ---
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text.strip()[:20].replace(" ", "_") or "audio"
    output_path = f"temp/{my_file_name}.mp3"
    tts.save(output_path)
    return output_path

# --- BOTÓN DE CONVERSIÓN ---
if st.button("🎙️ Convertir a Audio"):
    if text.strip() == "":
        st.warning("⚠️ Por favor ingresa algún texto antes de continuar.")
    else:
        with st.spinner("🎶 Generando tu audio..."):
            audio_path = text_to_speech(text, lg)
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.success("✅ ¡Conversión completa!")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            # --- DESCARGA DEL ARCHIVO ---
            with open(audio_path, "rb") as f:
                data = f.read()

            bin_str = base64.b64encode(data).decode()
            href = (
                f'<a href="data:application/octet-stream;base64,{bin_str}" '
                f'download="{os.path.basename(audio_path)}">⬇️ Descargar audio</a>'
            )
            st.markdown(href, unsafe_allow_html=True)

# --- LIMPIEZA AUTOMÁTICA DE ARCHIVOS ---
def remove_files(days_old):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    for f in mp3_files:
        if os.stat(f).st_mtime < now - (days_old * 86400):
            os.remove(f)

remove_files(7)

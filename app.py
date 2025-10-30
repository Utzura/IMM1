import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ---------- CONFIGURACIÓN DE PÁGINA ----------
st.set_page_config(page_title="🎧 Conversión de Texto a Audio", page_icon="🎙️", layout="centered")

# ---------- ESTILO PERSONALIZADO ----------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #F2E6FF, #E0F7FA);
        color: #222;
    }
    .stButton>button {
        background-color: #6C63FF;
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #574BFF;
        transform: scale(1.03);
    }
    .sidebar .sidebar-content {
        background: #F4F0FF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TÍTULO ----------
st.title("🎧 Conversión de Texto a Audio")

# ---------- IMAGEN PRINCIPAL ----------
image = Image.open('gato_raton.png')
st.image(image, width=350)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("📚 Texto de ejemplo")
    st.info("Escribe o selecciona el texto que quieres escuchar.")
    
    try:
        os.mkdir("temp")
    except:
        pass

    st.subheader("Una pequeña fábula de Franz Kafka")
    st.write(
        "“¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. "
        "Al principio era tan grande que le tenía miedo. Corría y corría "
        "y me alegraba ver esos muros, a diestra y siniestra, en la distancia. "
        "Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto "
        "y ahí en el rincón está la trampa sobre la cual debo pasar. "
        "Todo lo que debes hacer es cambiar de rumbo —dijo el gato—... y se lo comió.”"
    )

# ---------- INPUT PRINCIPAL ----------
st.markdown("### ✍️ Ingresa el texto que quieres convertir en audio")
text = st.text_area("Texto a escuchar", placeholder="Escribe o pega tu texto aquí...")

# ---------- IDIOMA ----------
option_lang = st.selectbox("🌎 Selecciona el idioma", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# ---------- CONVERSIÓN ----------
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# ---------- BOTÓN CONVERTIR ----------
if st.button("🔊 Convertir a Audio"):
    if text.strip() == "":
        st.warning("⚠️ Por favor escribe algún texto antes de convertir.")
    else:
        result, output_text = text_to_speech(text, 'com', lg)
        audio_path = f"temp/{result}.mp3"

        # Mostrar reproductor de audio
        st.success("✅ ¡Tu audio está listo!")
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Descarga del archivo
        with open(audio_path, "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='Archivo'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="color:#574BFF;font-weight:bold;">⬇️ Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(audio_path, "Archivo de audio"), unsafe_allow_html=True)

# ---------- LIMPIEZA AUTOMÁTICA ----------
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

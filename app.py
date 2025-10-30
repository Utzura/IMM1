import streamlit as st
import speech_recognition as sr
import pyttsx3
from PIL import Image
import pytesseract
import urllib.request
import io

# --- Configuración general ---
st.set_page_config(page_title="Interfaz Multimodal", page_icon="🎙️", layout="centered")

st.title("🎙️ Interfaz Multimodal Inteligente")
st.caption("Explora las funciones de texto, voz e imagen en un mismo espacio interactivo.")

# --- Menú lateral ---
opcion = st.sidebar.radio(
    "Selecciona una función:",
    ["🗣️ Voz a texto", "💬 Texto a voz", "🖼️ Análisis de imagen", "📄 OCR (leer texto en imagen)"]
)

# --- VOZ A TEXTO ---
if opcion == "🗣️ Voz a texto":
    st.header("🎤 Voz a texto")
    st.write("Convierte tu voz en texto usando el micrófono.")

    if st.button("Grabar y transcribir"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Escuchando... habla claramente.")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            st.success("✅ Transcripción:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("No se entendió lo que dijiste.")
        except sr.RequestError:
            st.error("Error con el servicio de reconocimiento de voz.")

# --- TEXTO A VOZ ---
elif opcion == "💬 Texto a voz":
    st.header("🗣️ Texto a voz")
    st.write("Convierte texto escrito en voz.")

    text = st.text_area("Escribe algo:", "Hola, esto es una prueba de voz generada por IA.")
    if st.button("Reproducir voz"):
        engine = pyttsx3.init()
        st.info("🔊 Reproduciendo...")
        engine.say(text)
        engine.runAndWait()

# --- ANÁLISIS DE IMAGEN ---
elif opcion == "🖼️ Análisis de imagen":
    st.header("🖼️ Análisis visual de una obra")
    st.write("Explora una imagen y reflexiona sobre su contenido artístico o emocional.")

    # Imagen desde Unsplash (para evitar error 403)
    image_url = "https://images.unsplash.com/photo-1505664194779-8beaceb93744"
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        img = Image.open(io.BytesIO(img_data))
        st.image(img, width=400, caption="The Thinker — Auguste Rodin (Unsplash)")
    except Exception as e:
        st.error(f"No se pudo cargar la imagen: {e}")
        st.info("El pensador es algo irrepensentable, realmente podemos tener una verisón física del pensamiento?")

# --- OCR (LECTURA DE TEXTO EN IMÁGENES) ---
elif opcion == "📄 OCR (leer texto en imagen)":
    st.header("📄 Reconocimiento de texto en imágenes")
    st.write("Sube una imagen con texto para extraer su contenido automáticamente.")

    uploaded_file = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_container_width=True)

        if st.button("📜 Leer texto"):
            try:
                text = pytesseract.image_to_string(image, lang="spa")
                if text.strip():
                    st.success("✅ Texto detectado:")
                    st.write(text)
                else:
                    st.warning("No se detectó texto en la imagen.")
            except Exception as e:
                st.error(f"Error al procesar la imagen: {e}")



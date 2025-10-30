import streamlit as st
from PIL import Image
import urllib.request
import io

# --- Configuración inicial de la app ---
st.set_page_config(page_title="Arte y Reflexión", page_icon="🎨", layout="centered")

st.title("🎨 Galería Interactiva de Arte")
st.subheader("Una experiencia de exploración visual y reflexiva")

# --- Cargar imagen desde Unsplash ---
image_url = "https://images.unsplash.com/photo-1505664194779-8beaceb93744"

try:
    # Crear un request con headers (para evitar bloqueos)
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        img_data = response.read()
    img = Image.open(io.BytesIO(img_data))
    st.image(img, width=350, caption="The Thinker — Auguste Rodin (Unsplash)")
except Exception as e:
    st.error(f"No se pudo cargar la imagen: {e}")

# --- Contenido interactivo ---
st.write("Esta aplicación muestra una obra representativa del pensamiento humano y permite reflexionar sobre su significado.")

if st.button("💭 Mostrar reflexión"):
    st.info("El pensador representa la búsqueda interior del ser humano, la duda y la contemplación del conocimiento.")

# --- Pie de página ---
st.divider()
st.caption("App desarrollada con Streamlit | Ejemplo educativo")

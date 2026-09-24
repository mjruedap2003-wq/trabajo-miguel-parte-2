import base64
import glob
import os
import time
from gtts import gTTS
from PIL import Image
import streamlit as st

# -------------------------------------------------------------
# CONFIGURACIÓN Y ESTILOS AVANZADOS (DARK / POP ART STUDIO)
# -------------------------------------------------------------
st.set_page_config(
    page_title="VocalStudio AI ⚡ Production Hub", page_icon="🎙️", layout="wide"
)

# Crear directorio temporal si no existe
os.makedirs("temp", exist_ok=True)


def remove_old_files(days=1):
    now = time.time()
    cutoff = days * 86400
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - cutoff:
            try:
                os.remove(f)
            except OSError:
                pass


remove_old_files(1)


def generate_audio(text_content, lang_code, slow_speed=False):
    safe_name = "".join(
        c for c in text_content[:15] if c.isalnum() or c in (" ", "_")
    ).rstrip()
    if not safe_name:
        safe_name = "audio_vocalstudio"

    file_path = f"temp/{safe_name}_{int(time.time())}.mp3"
    tts = gTTS(text=text_content, lang=lang_code, slow=slow_speed)
    tts.save(file_path)
    return file_path


# CSS para convertir la app en un estudio creativo
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Inter:wght@400;600;800;900&display=swap');

    .stApp {
        background-color: #0f0f15;
        background-image: radial-gradient(#ff0055 15%, transparent 15%), radial-gradient(#00e5ff 15%, transparent 15%);
        background-position: 0 0, 10px 10px;
        background-size: 20px 20px;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    p, span, div, label, li {
        color: #f0f0f0 !important;
    }

    h1, h2, h3, .stTitle {
        font-family: 'Bangers', cursive !important;
        letter-spacing: 2px;
        color: #ff0055 !important;
        text-shadow: 3px 3px 0px #00e5ff, 6px 6px 0px #000000;
        text-transform: uppercase;
    }

    /* Tarjetas principales */
    div[data-testid="stColumn"] > div, .stTextArea {
        background-color: #181824;
        border: 3px solid #00e5ff;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 6px 6px 0px #000000;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #12121c !important;
        border-right: 4px solid #ff0055;
    }

    /* Botones de acción */
    .stButton>button {
        background-color: #ff0055 !important;
        color: #ffffff !important;
        font-family: 'Bangers', cursive !important;
        font-size: 1.5rem !important;
        padding: 10px 25px !important;
        border: 3px solid #000000 !important;
        border-radius: 10px !important;
        box-shadow: 5px 5px 0px #00e5ff !important;
        width: 100%;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translate(-3px, -3px);
        box-shadow: 8px 8px 0px #00e5ff !important;
        background-color: #00e5ff !important;
        color: #000000 !important;
    }

    /* Modificar área de texto */
    textarea {
        background-color: #0f0f15 !important;
        color: #00e5ff !important;
        font-size: 1.1rem !important;
        border: 2px solid #00e5ff !important;
        border-radius: 8px !important;
    }

    /* Imágenes */
    img {
        border: 3px solid #00e5ff !important;
        border-radius: 12px !important;
        box-shadow: 5px 5px 0px #000000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# SIDEBAR: PANEL DE CONTROL
# -------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ VOCAL STUDIO")
    st.write("---")
    st.header("⚙️ Configuración de Audio")

    idioma_sel = st.selectbox(
        "🌐 Idioma & Región:",
        options=[
            "Español (Latinoamérica)",
            "Español (España)",
            "English (US)",
            "English (UK)",
            "Deutsch (Alemán)",
        ],
    )

    modo_lectura = st.radio(
        "⚡ Velocidad / Estilo:",
        options=["Normal / Fluido", "Lento / Didáctico"],
    )

    st.write("---")
    st.markdown("### 💡 Plantillas Rápidas")
    plantilla = st.selectbox(
        "Cargar guión predeterminado:",
        options=[
            "Personalizado",
            "Fábula Kafka",
            "Trailer de Película",
            "Noticia de Impacto",
        ],
    )

# Mapeo de idioma
lang_code = "es"
if "English" in idioma_sel:
    lang_code = "en"
elif "Deutsch" in idioma_sel:
    lang_code = "de"

slow_speed = True if "Lento" in modo_lectura else False

# Textos de plantilla
textos_plantilla = {
    "Personalizado": "",
    "Fábula Kafka": "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. Corría y corría y por cierto que me alegraba ver esos muros... pero el gato le dijo: Todo lo que debes hacer es cambiar de rumbo... y se lo comió.",
    "Trailer de Película": "En un mundo dominado por Inteligencias Artificiales, un héroe inesperado emerge de las sombras para cambiar el destino de la humanidad. Este verano... no te pierdas el desenlace definitivo.",
    "Noticia de Impacto": "Última hora: Científicos logran establecer por primera vez comunicación en tiempo real con delfines utilizando algoritmos avanzados de IA.",
}

texto_inicial = textos_plantilla[plantilla]

# -------------------------------------------------------------
# CUERPO PRINCIPAL
# -------------------------------------------------------------
st.title("🎙️ VOCALSTUDIO AI ⚡ PRODUCTION HUB")
st.markdown("##### *Transforma texto en locuciones dinámicas e interactivas*")

col_main, col_preview = st.columns([2, 1])

with col_main:
    st.subheader("📝 Guión de Locución")
    texto_usuario = st.text_area(
        "Escribe o edita el texto a sintetizar:",
        value=texto_inicial,
        height=180,
        placeholder="Escribe algo increíble para darle voz...",
    )

    btn_generar = st.button("🚀 GENERAR AUDIO Y PRODUCIR")

with col_preview:
    st.subheader("🖼️ Arte de Portada")
    try:
        image = Image.open("gato_raton.png")
        st.image(image, use_container_width=True)
    except Exception:
        st.info("🎨 *Coloca 'gato_raton.png' en el directorio para previsualizar el arte.*")

# -------------------------------------------------------------
# PROCESAMIENTO Y REPRODUCTOR
# -------------------------------------------------------------
if btn_generar:
    if texto_usuario.strip():
        with st.spinner("🎧 Sintetizando voz en el estudio..."):
            path_audio = generate_audio(texto_usuario, lang_code, slow_speed)

            with open(path_audio, "rb") as f:
                audio_data = f.read()

            st.success("🎉 ¡Producción de Audio Finalizada!")

            col_aud, col_down = st.columns([2, 1])
            with col_aud:
                st.audio(audio_data, format="audio/mp3")

            with col_down:
                b64 = base64.b64encode(audio_data).decode()
                href = f'<a href="data:file/mp3;base64,{b64}" download="vocalstudio_export.mp3" style="text-decoration:none;"><button style="padding: 12px 20px; background-color: #00e5ff; color: #000; border: 3px solid #000; border-radius: 8px; font-family: Bangers, cursive; font-size: 1.2rem; cursor: pointer; box-shadow: 4px 4px 0px #000;">📥 DESCARGAR MP3</button></a>'
                st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("⚠️ Ingresa un texto antes de presionar el botón de generación.")

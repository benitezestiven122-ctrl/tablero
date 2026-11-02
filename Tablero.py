import streamlit as st
import numpy as np
from PIL import Image
import io
from streamlit_drawable_canvas import st_canvas

# ==========================================
# 1. CONFIGURACIÓN Y ESTÉTICA (DARK / VJ THEME)
# ==========================================
st.set_page_config(
    page_title="Canvas-Synth | Asset Generator", 
    layout="wide", 
    page_icon="🎨"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background-color: #0b0c10 !important;
        color: #e5e5e5 !important;
    }
    
    h1, h2, h3 { color: #ff1e56 !important; }
    
    /* Acentos en Vinotinto y Rojo Carmesí */
    .stSlider > div > div > div > div { background-color: #ff1e56 !important; }
    
    .stButton > button {
        background: linear-gradient(135deg, #800020 0%, #b20038 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #b20038 0%, #ff1e56 100%) !important;
        box-shadow: 0 0 15px rgba(255, 30, 86, 0.5) !important;
    }
    
    .panel-info {
        background-color: #14080a;
        border-left: 4px solid #ff1e56;
        padding: 15px;
        border-radius: 4px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INTERFAZ PRINCIPAL
# ==========================================
st.title("🎨 Canvas-Synth: Generador de Máscaras")
st.markdown("Dibuja máscaras Alpha, Luma Mattes o Mapas de Desplazamiento para integrarlos en tiempo real a tus proyecciones de **Resolume**, **TouchDesigner** o texturas de **Blender**.")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3212/3212694.png", width=80)
    st.subheader("⚙️ Parámetros del Lienzo")
    
    # Resoluciones orientadas a video/3D
    formato = st.selectbox(
        "Relación de Aspecto (Aspect Ratio):",
        ("16:9 (Video HD - 720x405)", "1:1 (Textura 3D - 512x512)", "Libre")
    )
    
    if "16:9" in formato:
        canvas_width, canvas_height = 720, 405
    elif "1:1" in formato:
        canvas_width, canvas_height = 512, 512
    else:
        canvas_width = st.slider("Ancho (px)", 256, 1024, 600, 64)
        canvas_height = st.slider("Alto (px)", 256, 1024, 400, 64)

    st.divider()
    
    st.subheader("🛠️ Herramientas")
    # Mapeo de herramientas a formato amigable
    herramientas = {
        "Pincel Libre": "freedraw",
        "Trazado Lineal": "line",
        "Rectángulo / Máscara": "rect",
        "Círculo / Foco": "circle",
        "Polígono": "polygon",
        "Selector / Transformar": "transform"
    }
    herramienta_sel = st.selectbox("Modo de Interacción:", list(herramientas.keys()))
    drawing_mode = herramientas[herramienta_sel]

    stroke_width = st.slider("Grosor del Trazo / Difuminado", 1, 100, 15)
    
    col1, col2 = st.columns(2)
    with col1:
        stroke_color = st.color_picker("Color Base", "#FFFFFF")
    with col2:
        bg_color = st.color_picker("Color de Fondo", "#000000") # Negro por defecto para Alpha
        
    st.caption("💡 **Tip:** Usa blanco sobre fondo negro para crear Luma Mattes perfectos.")

# ==========================================
# 3. COMPONENTE DEL TABLERO
# ==========================================
col_canvas, col_render = st.columns([2, 1])

with col_canvas:
    st.write(f"**Lienzo Activo** ({canvas_width}x{canvas_height} px)")
    canvas_result = st_canvas(
        fill_color="rgba(255, 30, 86, 0.3)", # Relleno carmesí translúcido para polígonos
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key="canvas_synth", 
    )

# ==========================================
# 4. PROCESAMIENTO Y EXPORTACIÓN
# ==========================================
with col_render:
    st.write("### 📤 Render de Salida")
    
    if canvas_result is not None and canvas_result.image_data is not None:
        # Extraer los datos de la imagen generada
        img_array = canvas_result.image_data
        
        # Convertir a imagen de Pillow para manipulación y descarga
        img_pil = Image.fromarray(img_array.astype('uint8'), 'RGBA')
        
        st.image(img_pil, use_container_width=True, caption="Asset Generado")
        
        # Preparar la imagen para descarga
        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descargar Asset (PNG)",
            data=byte_im,
            file_name="canvas_synth_mask.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.markdown(f"""
        <div class="panel-info">
            <b>Integración en tu Pipeline:</b><br>
            • <b>Blender:</b> Conecta este PNG al nodo <i>Displacement</i> para crear relieve.<br>
            • <b>Resolume/AE:</b> Úsalo en la capa superior y activa el modo de mezcla <i>Luma Key / Silhouette Luma</i> para enmascarar tus videos.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Dibuja en el lienzo para generar el pre-renderizado.")

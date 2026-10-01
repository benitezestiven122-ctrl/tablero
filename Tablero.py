import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Tablero Interactivo", 
    page_icon="🎨", 
    layout="wide"
)

st.title("🎨 Tablero de Dibujo Interactivo")
st.markdown("Dibuja libremente, crea figuras geométricas o sube una imagen para dibujar sobre ella.")

# ==========================================
# 2. BARRA LATERAL (CONTROLES Y PARÁMETROS)
# ==========================================
with st.sidebar:
    st.header("Herramientas de Dibujo 🛠️")
    
    # Seleccionar la herramienta
    herramienta = st.selectbox(
        "Modo de dibujo:", 
        ("Trazo libre", "Línea", "Rectángulo", "Círculo", "Polígono", "Punto", "Transformar/Mover")
    )
    
    # Diccionario para mapear la opción en español con el comando que requiere el canvas
    modos_canvas = {
        "Trazo libre": "freedraw",
        "Línea": "line",
        "Rectángulo": "rect",
        "Círculo": "circle",
        "Polígono": "polygon",
        "Punto": "point",
        "Transformar/Mover": "transform"
    }
    drawing_mode = modos_canvas[herramienta]

    st.divider()

    # Controles de color y grosor
    stroke_width = st.slider("Grosor del trazo:", 1, 25, 3)
    
    col1, col2 = st.columns(2)
    with col1:
        stroke_color = st.color_picker("Color del trazo:", "#000000")
    with col2:
        bg_color = st.color_picker("Color de fondo:", "#FFFFFF")

    st.divider()

    # Opción para subir una imagen de fondo
    st.write("🖼️ **Imagen de fondo (Opcional)**")
    bg_image_file = st.file_uploader("Sube una imagen:", type=["png", "jpg", "jpeg"])
    bg_image = Image.open(bg_image_file) if bg_image_file else None

    # Parámetro extra si se usa la herramienta "Punto"
    punto_radio = st.slider("Radio del punto:", 1, 25, 3) if drawing_mode == "point" else 0

    realtime_update = st.checkbox("Actualizar en tiempo real", True)

# ==========================================
# 3. ÁREA PRINCIPAL (CANVAS)
# ==========================================
# Aquí renderizamos el tablero con todos los parámetros recopilados en la barra lateral
st.write("### Lienzo")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno de las figuras (naranja semitransparente)
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=bg_image,
    update_streamlit=realtime_update,
    height=500,               # Altura del tablero
    width=800,                # Anchura del tablero
    drawing_mode=drawing_mode,
    point_display_radius=punto_radio,
    key="canvas",             # Llave única requerida por Streamlit
)

# ==========================================
# 4. PROCESAMIENTO DEL RESULTADO (OPCIONAL)
# ==========================================
# Esto es muy útil si quieres usar el dibujo para pasarlo a un modelo de IA (Ej: YOLO o CNN)
if canvas_result.image_data is not None:
    with st.expander("Ver datos de la imagen generada (Para IA o Backend)"):
        st.write("Matriz de la imagen (NumPy array):")
        st.dataframe(canvas_result.image_data)
        
        st.write("Detalles de los vectores (JSON):")
        st.json(canvas_result.json_data)

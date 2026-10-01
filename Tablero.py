import streamlit as st
from streamlit_drawable_canvas import st_canvas

# 1. Configuración de la página
st.set_page_config(page_title="Tablero de Dibujo", layout="wide", page_icon="🎨")

st.title("🎨 Tablero para dibujo")

with st.sidebar:
    st.subheader("Propiedades del Tablero")

    # Dimensiones del tablero
    st.write("**Dimensiones**")
    canvas_width = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero", 200, 600, 300, 50)

    # Selector de modo de dibujo
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point")
    )

    # Controles de trazo y color
    stroke_width = st.slider("Selecciona el ancho de línea", 1, 30, 15)
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")
    bg_color = st.color_picker("Color de fondo", "#000000")

# 2. Creación del componente con una 'key' ESTÁTICA
# Esto evita que el lienzo se borre al cambiar las dimensiones en el menú lateral
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="my_canvas", 
)

# 3. Mostrar o utilizar el resultado del dibujo de forma segura
if canvas_result is not None:
    try:
        # Intenta acceder a la imagen. 
        # Si el componente de React aún no ha devuelto los datos (primer render), 
        # se capturará el RuntimeError.
        if canvas_result.image_data is not None:
            st.markdown("---")
            st.subheader("🖼️ Previsualización de la Imagen Generada")
            # Muestra el array de NumPy devuelto por el lienzo como una imagen
            st.image(canvas_result.image_data)
            
    except RuntimeError:
        # Ignoramos el error silenciosamente para que la app termine 
        # de cargar correctamente. 
        pass

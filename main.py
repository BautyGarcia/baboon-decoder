import streamlit as st
from PIL import Image
from decoding import decodeImage

# Sidebar for title and introductory text
st.sidebar.header("Desencriptador de Babuinos")
st.sidebar.write("¿Nunca te pasó de tener una foto de un babuino, pero está encriptada?")
st.sidebar.write("¡No te preocupes! Con esta herramienta podrás desencriptarla (si está bien encriptada).")

# Main area for the decoder
st.header("Pasame tu baboon", anchor=False)
data = st.file_uploader("Subir archivo", label_visibility="hidden", type=['png', 'jpg', 'jpeg'])

if data is not None:
    # Display the uploaded image
    st.image(data, caption='Imagen cargada.', use_column_width=True)
    
    # Button to decode the image
    if st.button('Desencriptar'):
        try:
            result = decodeImage(Image.open(data))

            # Use a container to create a styled section for displaying the result
            with st.container():
                st.markdown("""
                    <style>
                    .result-container {
                        background-color: #262730;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0px;
                    }
                    .subres {
                        font-size: 20px;
                        font-weight: bolder;
                        color: #f0f0f0;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                
                # Display the result inside the styled container
                if result:
                    st.markdown(f"<div class='result-container'><p class='subres'>Esto es lo que pude encontrar:</p><p style='font-size: 30px; font-weight: bold;'>{result}</p></div>", unsafe_allow_html=True)
                else:
                    st.error("Lo intenté, pero no pude encontrar nada.")
        except Exception as e:
            st.error("No che, algo no funciona bien, asegúrate de que la imagen esté bien encriptada.")
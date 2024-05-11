import streamlit as st
from PIL import Image
from decoding import decodeImage

# Sidebar for title and introductory text
st.sidebar.header("Desencriptador de Babuinos")
st.sidebar.write("¿Nunca te pasó de tener una foto de un babuino, pero está encriptada?")
st.sidebar.write("¡No te preocupes! Con esta herramienta podrás desencriptarla (si está bien encriptada).")

# Main area for the decoder
st.header("Carga tu imagen")
data = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if data is not None:
    # Display the uploaded image
    st.image(data, caption='Imagen cargada.', use_column_width=True)
    
    # Button to decode the image
    if st.button('Desencriptar'):
        # Call the decodeImage function with the file path
        
        try:
            result = decodeImage(Image.open(data))
            # Display the result
            st.write("Resultado de la desencriptación:")
            st.write(result if result else "No se encontró nada en la imagen.")
            
        except Exception as e:
            st.write("No che, algo no funciona bien, Asegúrate de que la imagen esté bien encriptada.")

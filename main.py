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
        # Call the decodeImage function with the file path
        
        try:
            result = decodeImage(Image.open(data))
            # Display the result
            st.write("Resultado de la desencriptación:")
            st.markdown(f"<p style='font-size: 30px; font-weight: bold;'>{result if result else "Lo intente, pero no pude encontrar nada"}</p>", unsafe_allow_html=True)
            
        except Exception as e:
            st.write("No che, algo no funciona bien, Asegúrate de que la imagen esté bien encriptada.")
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs

def app():
    portada = Image.open("images/Madrid-GranVia.jpg")
    st.image(portada, use_column_width=True)
    st.write("""
    # tiempos
    """)

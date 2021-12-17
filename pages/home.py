import streamlit as st
from PIL import Image

def app():
    portada = Image.open("images/Madrid-GranVia.jpg")
    st.image(portada, use_column_width=True)
    st.write("""
    # Análisis tiempos Uber MADRID
    
    Bienvenido.
    Con esta applicación podrás saber cuanto tiempo se tarda en llegar de un sitio a otro.
    Información sobre el tiempo de un trayecto ya lo tienes en Google Maps. 
    Aquí se ha buscado hacer un análisis estádistico sobre el histórico de trayectos de Uber en Madrid.
    Se comprueba la diferencia de tiempo entre unos días y otros, y la diferencia entre días laborables y fines de semana.
    También se analiza cómo evoluciona el tráfico a lo largo de los meses del año, e incluso también a lo largo del día.\n
    En "Me quiero escapar" puedes ver hasta donde puedes llegar desde un lugar y en un tiempo máximo.\n
    En "Tráfico ladrón de tiempo" puedes entender cómo influyen los horarios en tus trayectos rutinarios.
    
    """)



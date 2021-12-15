import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import src.manage_data as dat
import plotly.express as px

def app():
    st.write("""
    # org_dest
    """)
    
    searchby = st.sidebar.radio("Selecciona la forma de busqueda:" , ["Por Código Postal", "Por Barrio"]) 
    if searchby == "Por Código Postal" :
        searchby = True
        origin  = st.sidebar.selectbox("Selecciona el Código Postal de origen  :" , ["..."]+dat.origin()  ) 
        destiny = st.sidebar.selectbox("Selecciona el Código Postal de destino :" , ["..."]+dat.destiny() ) 
        
    elif searchby == "Por Barrio" :
        searchby = False
        origin_list = ["..."]+dat.origin()
        destiny_list = ["..."]+dat.origin()
        origin  = st.sidebar.selectbox("Selecciona el Barrio de origen  :" , origin_list  )
        if origin != "..." :
            destiny_list.remove(origin) 
        destiny = st.sidebar.selectbox("Selecciona el Barrio de destino :" , destiny_list ) 

    st.sidebar.write("Selecciona tipo de días a mostrar:")
    weekday  = st.sidebar.checkbox("Laborable") 
    weekend  = st.sidebar.checkbox("Fin de Semana") 
    if weekend == "Laborable" :
        weekend = False
    elif weekend == "Fin de Semana" :
        weekend = True

    year     = st.sidebar.selectbox("selecciona un año", ["..."]+dat.years())
        
    st.write("""
    Has elegido:
    """, year, searchby, weekday, weekend, origin, destiny )
    
    if ( (searchby == True or searchby == False ) & (origin != "...") & (destiny != "...") ) :
        run_button = st.sidebar.button("Refresh graph")
        if run_button :
            st.write("Refresh press!")
    
    

    #data_bar = dat.monthdf(year)
    #fig = px.bar(data_bar, y="omean_time_m")
    #st.plotly_chart(fig)


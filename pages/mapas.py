import streamlit as st
from streamlit_folium import folium_static
import streamlit.components.v1 as components
import codecs
import folium
import requests
from src.geocoding import consigue_lat_long


def app():
    st.write("""
    # MAPAS
    """)
    
    size_mapa = st.sidebar.slider("Zoom del mapa :",min_value = 9 , max_value=15, step=1, value = 12)
    tipo_mapa = st.sidebar.radio("Selecciona la forma de busqueda:" , ['OpenStreetMap', 
                                                                       'Stamen Terrain', 
                                                                       'Stamen Toner', 
                                                                       'TomTom', 
                                                                       'Image', 
                                                                       'WaterColor']) 
    if   tipo_mapa == 'OpenStreetMap' :
        tiles_mapa = 'OpenStreetMap'
        attr_mapa  = ''

    elif tipo_mapa == 'Stamen Terrain' :
        tiles_mapa = 'Stamen Terrain'
        attr_mapa  = ''

    elif tipo_mapa == 'Stamen Toner' :
        tiles_mapa = 'Stamen Toner'
        attr_mapa  = ''

    elif tipo_mapa == 'TomTom' :
        tiles_mapa = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
        attr_mapa  = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'

    elif tipo_mapa == 'Image' :
        tiles_mapa = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        attr_mapa  = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'

    if tipo_mapa == 'WaterColor' :
        tiles_mapa = 'https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg'
        attr_mapa  = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'

        
    default_value_goes_here = "Puerta del Sol, Madrid"
    user_input = st.text_input("Introduce dirección", default_value_goes_here)
    latlon = consigue_lat_long(user_input)

    icono = folium.Icon(color="blue",
             prefix = "fa",
             icon="rocket",
             icon_color="black")
    datos = {"location": latlon, "tooltip": "Lo que buscas", "icon":icono}
    mark = folium.Marker(**datos)


    map_1 = folium.Map(location = latlon, zoom_start=size_mapa, tiles=tiles_mapa , attr=attr_mapa)
    mark.add_to(map_1)

    folium_static(map_1)

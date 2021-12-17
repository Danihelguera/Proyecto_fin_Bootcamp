import streamlit as st
from   streamlit_folium import folium_static
import folium
from   src.geocoding import consigue_lat_long
from   src.geocoding import consigue_type_point_lat_long
from   src.geocoding import permutar_lat_x_long
from   src.geocoding import buscar_barrio
from   src.geocoding import buscar_codigo_postal
import src.manage_data as dat
import branca.colormap as cmp
import json



def app():
    default_origin = "Puerta del Sol, Madrid"
    origin = st.sidebar.text_input("Introduce Origen", default_origin)
    origin_ll = consigue_lat_long(origin)
    origin_ll_T = permutar_lat_x_long(consigue_type_point_lat_long(origin_ll))

    search_by = {}
    search_by["origin"]  = int(buscar_barrio(origin_ll_T))
    if search_by["origin"] != False :
        search_by["tipo"]    = "barrio"
        geo_json = json.load( open ("data/madrid_barrios.geojson") )
        style_function = lambda feature: {'fillColor': step(dict_time_to_destiny[feature["properties"]['DISPLAY_NAME']]) , 'weight': 1}

    else :
        search_by["origin"]  = int(buscar_codigo_postal(origin_ll_T))
        if search_by["origin"] != False :
            search_by["tipo"]    = "codigo_postal"
            geo_json = json.load( open ("data/madrid_codigos_postales.geojson") )
            style_function = lambda feature: {'fillColor': step(dict_time_to_destiny[feature["properties"]['GEOCODIGO']]) , 'weight': 1 }
        else   :         
            search_by["tipo"]    = "Fuera de rango geografico (Comunidad de Madrid)"
            search_by["origin"]  = "No encontrado"
            st.write(search_by["tipo"])
        
    tiempo_max = st.sidebar.slider("Tiempo máximo en coche en minutos:",min_value = 1 , max_value=90, step=1, value = 15)
    st.write(f"# Me quiero escapar... \n## a {tiempo_max} minutos de aquí")
        
    tipo_mapa = st.sidebar.radio("Selecciona la forma de busqueda:" , ['OpenStreetMap', 
                                                                       'Stamen Terrain', 
                                                                       'Stamen Toner', 
                                                                       'TomTom', 
                                                                       'Image', 
                                                                       'WaterColor'], index = 2) 
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
    size_mapa = st.sidebar.slider("Zoom del mapa :",min_value = 8 , max_value=16, step=1, value = 12)

    dict_time_to_destiny = dat.carga_dict_time_todos_los_destinos(search_by)
    
    vmin = dict_time_to_destiny.values.min()
    vmax = tiempo_max
    step = cmp.StepColormap(['green','yellow', 'red'], 
                            vmin=vmin, 
                            vmax=vmax, 
                            index=[ vmin , vmin+0.7*(vmax-vmin), vmin+0.95*(vmax-vmin), vmax ],  #for change in the colors, not used fr linear
                            caption='Color Scale for Map'    #Caption for Color scale or Legend 
                            )
       
        
    origin_icon = folium.Icon(color="blue",
                              prefix = "fa",
                              icon="rocket",
                              icon_color="black")
    origin_icon_data  = {"location": origin_ll, "tooltip": "Origen", "icon":origin_icon}
    origin_mark = folium.Marker(**origin_icon_data)
    map_1 = folium.Map(location = origin_ll, zoom_start=size_mapa, tiles=tiles_mapa , attr=attr_mapa)
    origin_mark.add_to(map_1)
    
    folium.GeoJson(geo_json, style_function=style_function ).add_to(map_1)
    folium_static(map_1)
    
    st.write(step)
    
    


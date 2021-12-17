import streamlit as st
from   streamlit_folium import folium_static
import folium
import math
from   src.geocoding import consigue_lat_long
from   src.geocoding import consigue_type_point_lat_long
from   src.geocoding import permutar_lat_x_long
from   src.geocoding import buscar_barrio
from   src.geocoding import buscar_codigo_postal
import src.manage_data as dat
from   pymongo import MongoClient
import seaborn as sns
from   matplotlib.figure import Figure


def app():
    default_origin = "Boadilla del Monte"
    origin = st.sidebar.text_input("Introduce Origen", default_origin)
    origin_ll = consigue_lat_long(origin)
    origin_ll_T = permutar_lat_x_long(consigue_type_point_lat_long(origin_ll))
    
    default_destiny = "Puerta del Sol, Madrid"
    destiny = st.sidebar.text_input("Introduce Destino", default_destiny)
    destiny_ll = consigue_lat_long(destiny)

    destiny_ll_T = permutar_lat_x_long(consigue_type_point_lat_long(destiny_ll))

    size_mapa = st.sidebar.slider("Zoom del mapa :",min_value = 9 , max_value=15, step=1, value = 12)
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

    st.write(f"# Tráfico ladrón de mi tiempo ...")

            
    search_by = {}
    search_by["origin"]  = int(buscar_barrio(origin_ll_T))
    search_by["destiny"] = int(buscar_barrio(destiny_ll_T))
    if (search_by["origin"] != False) and (search_by["destiny"] != False) :
        search_by["tipo"]    = "barrio"
    else :
        search_by["origin"]  = int(buscar_codigo_postal(origin_ll_T))
        search_by["destiny"] = int(buscar_codigo_postal(destiny_ll_T))
        if (search_by["origin"] != False) and (search_by["destiny"] != False) :
            search_by["tipo"]    = "codigo_postal"
        else   :         
            search_by["tipo"]    = "Fuera de rango geografico (Comunidad de Madrid)"
            search_by["origin"]  = "No encontrado"
            search_by["destiny"] = "No encontrado"

    if   search_by["tipo"] == "Fuera de rango geografico (Comunidad de Madrid)" :
        st.write(search_by)

    else:
        client = MongoClient("localhost:27017")
        db = client.get_database("Coropleticos_Madrid")
        if search_by["tipo"] == "barrio" :
            c  = db.get_collection("Barrios")
        elif search_by["tipo"] == "codigo_postal" :
            c  = db.get_collection("Codigos_Postales")
        geo_Reduced = {'type'    : 'FeatureCollection', 'features': [] }
        query = {"geometry": {"$geoIntersects": {"$geometry": origin_ll_T}}}
        origin_geo = c.find_one(query)
        origin_geo.pop('_id')
        geo_Reduced["features"].append(origin_geo)
        query = {"geometry": {"$geoIntersects": {"$geometry": destiny_ll_T}}}
        destiny_geo = c.find_one(query)
        destiny_geo.pop('_id')
        geo_Reduced["features"].append(destiny_geo)
        
        origin_icon = folium.Icon(color="blue",
                                  prefix = "fa",
                                  icon="rocket",
                                  icon_color="black")
        origin_icon_data  = {"location": origin_ll, "tooltip": "Origen", "icon":origin_icon}
        origin_mark = folium.Marker(**origin_icon_data)
        destiny_icon = folium.Icon(color="red",                          
                                   prefix = "fa",
                                   icon="rocket",
                                   icon_color="black")
        destiny_icon_data = {"location": destiny_ll, "tooltip": "Destino", "icon":destiny_icon}
        destiny_mark = folium.Marker(**destiny_icon_data)
        punto_central = [(origin_ll[0]+destiny_ll[0])/2 , (origin_ll[1]+destiny_ll[1])/2 ]
        map_1 = folium.Map(location = punto_central, zoom_start=size_mapa, tiles=tiles_mapa , attr=attr_mapa)
        origin_mark.add_to(map_1)
        destiny_mark.add_to(map_1)
        

        style_function = lambda feature: {'fillColor': 'blue',
                                        'color': 'blue',
                                        'weight': 1}
        
        folium.GeoJson(geo_Reduced, style_function=style_function ).add_to(map_1)
        folium_static(map_1)

        st.write(" ")
        
        Wdf_to_plot = dat.carga_df_weekly(search_by)
        Hdf_to_plot = dat.carga_df_hourly(search_by)
        Mdf_to_plot = dat.carga_df_monthly(search_by)
       
        ymin = min( Wdf_to_plot["y"].min(), Hdf_to_plot[["Media Total","Laborables","Fin de semana"]].min().min() , Mdf_to_plot[["Media Total","Laborables","Fin de semana"]].min().min() )
        ymax = max( Wdf_to_plot["y"].max(), Hdf_to_plot[["Media Total","Laborables","Fin de semana"]].max().max() , Mdf_to_plot[["Media Total","Laborables","Fin de semana"]].max().max() )
        ylim_low  = math.floor( ymin-0.1*(ymax-ymin) )
        ylim_high = math.ceil(  ymax+0.1*(ymax-ymin) )
        
        fig1 = Figure( figsize = (15,15) )
        fig1.suptitle("Tiempo medio IDA", fontsize=28,position=(0.5, 0.95))
        ax1,ax2,ax3 = fig1.subplots(3,1, sharey=True, squeeze=True)
        g = sns.barplot( data=Wdf_to_plot , x="x", y="y", ci="sd", palette="deep", alpha=.6 , ax=ax1);
        g.set(ylim=( ylim_low , ylim_high ) )
        ax1.set_title("Segun DIA DE LA SEMANA",loc='left')
        ax1.set_xticklabels(['L','M','X','J','V','S','D'])
        ax1.set_xlabel("")
        ax1.set_ylabel("Minutos");        

        g = sns.lineplot(data=Hdf_to_plot.drop(columns="Media Total").set_index("x"), palette="pastel", linewidth=1.5 , ax=ax2)
        g.fill_between( Hdf_to_plot["x"]  , 0 , Hdf_to_plot["Laborables"], alpha=0.3)
        g.fill_between( Hdf_to_plot["x"]  , 0 , Hdf_to_plot["Fin de semana"], alpha=0.3)
        g = sns.lineplot(data=Hdf_to_plot.drop(columns=["Laborables","Fin de semana"]).set_index("x"), linewidth=3 , palette=['green'] , ax=ax2)
        g.set(ylim=( ylim_low , ylim_high ) )
        g.set(xticks=[0,4,8,12,16,20,23])
        ax2.set_title("Segun HORA DEL DIA",loc='left')
        ax2.set_xlabel("")
        ax2.set_ylabel("Minutos");        

        g = sns.lineplot(data=Mdf_to_plot.drop(columns="Media Total").set_index("x"), palette="pastel", linewidth=1.5 , ax=ax3 )
        g.fill_between( Mdf_to_plot["x"]  , 0 , Mdf_to_plot["Laborables"], alpha=0.3)
        g.fill_between( Mdf_to_plot["x"]  , 0 , Mdf_to_plot["Fin de semana"], alpha=0.3)
        g = sns.lineplot(data=Mdf_to_plot.drop(columns=["Laborables","Fin de semana"]).set_index("x"), linewidth=3 , palette=['green'] , ax=ax3 )
        g.set(ylim=( ylim_low , ylim_high ) )
        ax3.set_title("Segun MES",loc='left')
        ax3.set_xlabel("")
        ax3.set_ylabel("Minutos")
        st.pyplot(fig1)


        search_by = {"tipo"    : search_by["tipo"]    ,
                     "origin"  : search_by["destiny"] , 
                     "destiny" : search_by["origin"]  }
        Wdf_to_plot = dat.carga_df_weekly(search_by)
        Hdf_to_plot = dat.carga_df_hourly(search_by)
        Mdf_to_plot = dat.carga_df_monthly(search_by)
       
        ymin = min( Wdf_to_plot["y"].min(), Hdf_to_plot[["Media Total","Laborables","Fin de semana"]].min().min() , Mdf_to_plot[["Media Total","Laborables","Fin de semana"]].min().min() )
        ymax = max( Wdf_to_plot["y"].max(), Hdf_to_plot[["Media Total","Laborables","Fin de semana"]].max().max() , Mdf_to_plot[["Media Total","Laborables","Fin de semana"]].max().max() )
        ylim_low  = math.floor( ymin-0.1*(ymax-ymin) )
        ylim_high = math.ceil(  ymax+0.1*(ymax-ymin) )

        st.write(" ")
        fig2 = Figure( figsize = (15,15) )
        fig2.suptitle("Tiempo medio VUELTA", fontsize=28,position=(0.5, 0.95))
        ax1,ax2,ax3 = fig2.subplots(3,1, sharey=True, squeeze=True)
        g = sns.barplot( data=Wdf_to_plot , x="x", y="y", ci="sd", palette="deep", alpha=.6 , ax=ax1);
        g.set(ylim=( ylim_low , ylim_high ) )
        ax1.set_title("Segun DIA DE LA SEMANA",loc='left')
        ax1.set_xticklabels(['L','M','X','J','V','S','D'])
        ax1.set_xlabel("")
        ax1.set_ylabel("Minutos");        

        g = sns.lineplot(data=Hdf_to_plot.drop(columns="Media Total").set_index("x"), palette="pastel", linewidth=1.5 , ax=ax2)
        g.fill_between( Hdf_to_plot["x"]  , 0 , Hdf_to_plot["Laborables"], alpha=0.3)
        g.fill_between( Hdf_to_plot["x"]  , 0 , Hdf_to_plot["Fin de semana"], alpha=0.3)
        g = sns.lineplot(data=Hdf_to_plot.drop(columns=["Laborables","Fin de semana"]).set_index("x"), linewidth=3 , palette=['green'] , ax=ax2)
        g.set(ylim=( ylim_low , ylim_high ) )
        g.set(xticks=[0,4,8,12,16,20,23])
        ax2.set_title("Segun HORA DEL DIA",loc='left')
        ax2.set_xlabel("")
        ax2.set_ylabel("Minutos");        

        g = sns.lineplot(data=Mdf_to_plot.drop(columns="Media Total").set_index("x"), palette="pastel", linewidth=1.5 , ax=ax3 )
        g.fill_between( Mdf_to_plot["x"]  , 0 , Mdf_to_plot["Laborables"], alpha=0.3)
        g.fill_between( Mdf_to_plot["x"]  , 0 , Mdf_to_plot["Fin de semana"], alpha=0.3)
        g = sns.lineplot(data=Mdf_to_plot.drop(columns=["Laborables","Fin de semana"]).set_index("x"), linewidth=3 , palette=['green'] , ax=ax3 )
        g.set(ylim=( ylim_low , ylim_high ) )
        ax3.set_title("Segun MES",loc='left')
        ax3.set_xlabel("")
        ax3.set_ylabel("Minutos")
        st.pyplot(fig2)

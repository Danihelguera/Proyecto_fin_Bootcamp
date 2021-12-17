import pandas as pd
import streamlit as st
from datetime import datetime
import json

def carga_df_weekly(search_by):
    if search_by["tipo"] == "barrio" :
        df = pd.read_pickle("data/W_B_df.pkl")
    elif search_by["tipo"] == "codigo_postal" :
        df = pd.read_pickle("data/W_CP_df.pkl")
    df = df[(df.origin   == search_by["origin"]  ) & (df.destiny  == search_by["destiny"]  ) ]
    df = df.sort_values('dow')
    df = df.reset_index(drop=True)
    df_to_plot = pd.DataFrame()
    df_to_plot["x"] = df["dow"]
    df_to_plot["y"] = df["mean_time_s"]/60
    return df_to_plot

def carga_df_hourly(search_by):
    if search_by["tipo"] == "barrio" :
        df = pd.read_pickle("data/H_B_df.pkl")
    elif search_by["tipo"] == "codigo_postal" :
        df = pd.read_pickle("data/H_CP_df.pkl")
    df = df[(df.origin   == search_by["origin"]  ) & (df.destiny  == search_by["destiny"]  ) ]
    df = df.sort_values('hod')
    df = df.reset_index(drop=True)
    df_to_plot = pd.DataFrame()
    df_to_plot["x"]             = df["hod"]
    df_to_plot["Media Total"  ] = df["mean_time_s_ALL"]/60
    df_to_plot["Laborables"   ] = df["mean_time_s_WD"]/60
    df_to_plot["Fin de semana"] = df["mean_time_s_WE"]/60
    return df_to_plot

def carga_df_monthly(search_by):
    if search_by["tipo"] == "barrio" :
        df = pd.read_pickle("data/M_B_df.pkl")
    elif search_by["tipo"] == "codigo_postal" :
        df = pd.read_pickle("data/M_CP_df.pkl")
    df = df[(df.origin   == search_by["origin"]  ) & (df.destiny  == search_by["destiny"]  ) ]
    df = df.sort_values('date')
    df = df.reset_index(drop=True)
    df_to_plot = pd.DataFrame()
    df_to_plot["x"]             = df["date"]
    df_to_plot["Media Total"  ] = df["mean_time_s_ALL"]/60
    df_to_plot["Laborables"   ] = df["mean_time_s_WD" ]/60
    df_to_plot["Fin de semana"] = df["mean_time_s_WE" ]/60
    return df_to_plot

def carga_dict_time_todos_los_destinos(search_by) :
    if search_by["tipo"] == "barrio" :
        df = pd.read_pickle("data/W_B_df.pkl")
        geo_json = json.load( open ("data/madrid_barrios.geojson")          )
        areas = {}
        for id in range(len(geo_json["features"])) :
            cod = int(geo_json["features"][id]["properties"]["MOVEMENT_ID"])
            name = geo_json["features"][id]["properties"]["DISPLAY_NAME"]
            areas[cod] = name

    elif search_by["tipo"] == "codigo_postal" :
        df = pd.read_pickle("data/W_CP_df.pkl")
        geo_json = json.load( open ("data/madrid_codigos_postales.geojson") )
        areas = {}
        for id in range(len(geo_json["features"])) :
            cod = int(geo_json["features"][id]["properties"]["MOVEMENT_ID"])
            name = geo_json["features"][id]["properties"]["GEOCODIGO"]
            areas[cod] = name

    df = df[ (df.origin == search_by["origin"]) & ( df.dow == datetime.today().isoweekday())  ]
    df = df.sort_values('destiny')
    df = df.reset_index(drop=True)
    df_areas = pd.DataFrame.from_dict(areas,orient="index")
    df_areas.columns= ["area"]
    df_areas["mean_time_m"] = 1000
    for i,row in df.iterrows() :
        df_areas.loc[ [row["destiny"]], ["mean_time_m"]] = row["mean_time_s"]/60
        valores_dict = df_areas.set_index('area')['mean_time_m']
    return valores_dict
    

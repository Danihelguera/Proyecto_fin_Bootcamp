from geopy.geocoders import Nominatim
import json
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db = client.get_database("Coropleticos_Madrid")

def type_point(lista):
    return {"type":"Point", "coordinates": lista}

def consigue_lat_long(direccion):
    """
    Esta función saca las coordenadas de la dirección que le pases
    y la devuelve como lista [lat,long]
    """
    geolocator = Nominatim(user_agent="dddddddddddddddddd@gmail.com")
    location = geolocator.geocode(direccion)
    return [location.latitude, location.longitude]

def consigue_type_point_lat_long(direccion):
    """
    Esta función saca las coordenadas de la dirección que le pases
    y la devuelve en type:point 
    """
    return type_point( consigue_lat_long(direccion) )

def permutar_lat_x_long(lugar):
    lugar_T = type_point([lugar["coordinates"][1] , lugar["coordinates"][0] ])
    return lugar_T

def buscar_barrio(lugar) :
    query = {"geometry": {"$geoIntersects": {"$geometry": lugar}}}
    c    = db.get_collection("Barrios")
    proy = {"_id":0, "properties.DISPLAY_NAME": 1, "properties.MOVEMENT_ID": 1}
    try:
        return c.find_one(query,proy)["properties"]['MOVEMENT_ID']
    except:
        return False

def buscar_codigo_postal(lugar) :
    query = {"geometry": {"$geoIntersects": {"$geometry": lugar}}}
    c    = db.get_collection("Codigos_Postales")
    proy = {"_id":0, "properties.GEOCODIGO": 1   , "properties.MOVEMENT_ID": 1}
    try:
        return c.find_one(query,proy)["properties"]['MOVEMENT_ID']
    except:
        return False
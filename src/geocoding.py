from geopy.geocoders import Nominatim

def consigue_lat_long(user_input):
    geolocator = Nominatim(user_agent="dddddddddddddddddd@gmail.com")
    location = geolocator.geocode(user_input)
    return [location.latitude, location.longitude]
    
    
    
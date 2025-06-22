import requests

def get_lat_lon(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        res = requests.get(url).json()
        if res:
            lat = float(res[0]["lat"])
            lon = float(res[0]["lon"])
            return lat, lon
    except:
        pass
    return None, None

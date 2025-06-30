import requests

def get_lat_lon(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "mon-app-meteo/1.0 (contact@example.com)"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return None, None
    data = response.json()
    if not data:
        return None, None
    return float(data[0]["lat"]), float(data[0]["lon"])

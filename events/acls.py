import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    payload = {"query": f"{city}, {state}"}
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, params=payload, headers=headers)
    content = response.json()
    try:
        picture_url = content["photos"][0]["src"]["original"]
        return {"picture_url": picture_url}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather(city, state):
    # get latitude and longitude of city and state
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city}, {state}", "appid": OPEN_WEATHER_API_KEY}
    response = requests.get(url, params=params)
    content = response.json()
    latitude = content[0]["lat"]
    longitude = content[0]["lon"]

    # use the latitude and longitude to get the weather
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "units": "imperial",
        "appid": OPEN_WEATHER_API_KEY
        }
    response = requests.get(url, params=params)
    content = response.json()
    description = content["weather"][0]["description"]
    temp = content["main"]["temp"]
    return {"description": description, "temp": temp}
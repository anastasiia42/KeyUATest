import json

import requests


def get_weather(location):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"callback": "", "id": "2172797", "units": "%22metric%22 or %22imperial%22",
                   "mode": "xml%2C html", "q": "" + location + ""}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "0e3193e570msha97e0beec3ac38ap1d79e1jsn82eba06a2d0b"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return normalize_temperature(data["main"]["temp"])


def normalize_temperature(degrees):
    abs_zero = -273
    return round((float(degrees)) + abs_zero, 1)
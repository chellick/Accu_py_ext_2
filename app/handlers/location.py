import os
import requests
from dotenv import load_dotenv


def get_location_key_by_geoposition(latitude, longitude, api_key):
    """Получаем location_key для широты и долготы."""

    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={latitude},{longitude}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data["Key"]
        else:
            print("No location found.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def get_location_key_by_city(city_name, api_key):
    """Получаем location_key для города."""

    CITY_SEARCH_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"

    city_url = f"{CITY_SEARCH_URL}?apikey={api_key}&q={city_name}"
    response = requests.get(city_url)
    if response.status_code == 200:
        city_data = response.json()
        if city_data:
            return city_data[0]["Key"]  # Берем первый результат и получаем ключ
    return None


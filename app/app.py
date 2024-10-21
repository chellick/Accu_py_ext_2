from flask import Flask, jsonify, request, render_template
from handlers.location import get_location_key_by_geoposition, get_location_key_by_city
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
import os
from handlers.model import WeatherModel

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://dataservice.accuweather.com/currentconditions/v1/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check_weather", methods=["POST"])
def check_weather():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    city = request.form.get("city")

    location_key = None

    # Проверяем наличие широты и долготы и используем их с приоритетом
    try:
        if latitude and longitude:
            location_key = get_location_key_by_geoposition(latitude, longitude, API_KEY)
        # Если координаты не указаны, проверяем наличие города
        elif city:
            location_key = get_location_key_by_city(city, API_KEY)
        else:
            return jsonify({"error": "Please provide either latitude and longitude or city"}), 400

        # Если не удалось получить location_key
        if not location_key:
            return jsonify({"error": "Oops! Invalid city name or coordinates."}), 400

    except RequestException:
        return jsonify({"error": "Network error occurred while trying to get location key"}), 503
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    # Запрашиваем данные о погоде с использованием location_key
    weather_url = f"{BASE_URL}{location_key}?apikey={API_KEY}&details=true"

    try:
        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_data = response.json()

            # Логика обработки данных о погоде
            model = WeatherModel()
            model.parse_main_params(weather_data)
            parsed_data = model.weather_params
            parsed_data["weather_analysis"] = model.check_weather_params()

            return render_template("weather_result.html", weather=parsed_data)

        elif response.status_code == 404:
            return jsonify({"error": "Weather data not found for the given location"}), 404
        else:
            return jsonify({"error": "Failed to retrieve weather data from the server"}), response.status_code

    except RequestException:
        return jsonify({"error": "Network error occurred while trying to get weather data"}), 503
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=False)

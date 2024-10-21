import os
import requests
import json
from dotenv import load_dotenv




class WeatherModel:
    def __init__(self) -> None:
        self.weather_params = None
    
    
    def parse_main_params(self, weather_data: list):
        """Парсит основные параметры из загруженных данных"""
        
        self.weather_params = self.convert_weather_data_to_dict(weather_data)
        if "error" in self.weather_params:
            return {"error" : "Something went wrong..."}
        return {"accepted": "Valid weather params loaded"}
    
    
    @staticmethod
    def validate_weather_data(weather_data: list):
        """Проверяет, корректны ли входные данные о погоде"""
        
        if not isinstance(weather_data, list) or len(weather_data) == 0:
            return False, {"error": "Invalid weather data format"}
        return True, None


    @staticmethod
    def convert_weather_data_to_dict(weather_data: list):
        """Конвертирует данные о погоде в словарь с ключевыми параметрами"""
        
        is_valid, error = WeatherModel.validate_weather_data(weather_data)
        if not is_valid:
            return error
        
        weather = weather_data[0]

        weather_dict = {
            "Temperature (°C)": weather.get("Temperature", {}).get("Metric", {}).get("Value", None),
            "Apparent Temperature (°C)": weather.get("ApparentTemperature", {}).get("Metric", {}).get("Value", None),
            "Dew Point (°C)": weather.get("DewPoint", {}).get("Metric", {}).get("Value", None),
            "Wind Speed (km/h)": weather.get("Wind", {}).get("Speed", {}).get("Metric", {}).get("Value", None),
            "Wind Direction": weather.get("Wind", {}).get("Direction", {}).get("Localized", None),
            "Humidity (%)": weather.get("RelativeHumidity", None),
            "Precipitation Probability (%)": 100 if weather.get("HasPrecipitation", False) else 0,
            "Cloud Cover (%)": weather.get("CloudCover", None),
            "Visibility (km)": weather.get("Visibility", {}).get("Metric", {}).get("Value", None),
            "Pressure (mb)": weather.get("Pressure", {}).get("Metric", {}).get("Value", None),
            "UV Index": weather.get("UVIndex", None),
            "Weather Description": weather.get("WeatherText", None)
        }
        
        return weather_dict


    def get_weather_summary(self):
        """Возвращает краткий отчет о погоде, если данные были успешно загружены"""
        
        if self.weather_params:
            return json.dumps(self.weather_params, indent=4)
        return {"error": "Weather data is not loaded yet"}
    
    
    def check_weather_params(self):
        """Анализ погоды на основе загруженных параметров"""
        
        if not self.weather_params:
            return {"error": "No weather parameters loaded"}
        
        analysis = []
        
        temp = self.weather_params.get("Temperature (°C)")
        wind_speed = self.weather_params.get("Wind Speed (km/h)")
        precipitation_prob = self.weather_params.get("Precipitation Probability (%)")
        cloud_cover = self.weather_params.get("Cloud Cover (%)")
        
        if temp is not None:
            if temp < 0:
                analysis.append("Cold weather")
            elif temp < 10:
                analysis.append("Cool weather")
            elif temp > 35:
                analysis.append("Hot weather")
            else:
                analysis.append("Warm weather")
        
        if wind_speed is not None:
            if wind_speed > 30:
                analysis.append("Windy weather")
            elif wind_speed > 15:
                analysis.append("Moderate wind")
        
        if precipitation_prob is not None and precipitation_prob > 50:
            analysis.append("High chance of precipitation")
        
        if cloud_cover is not None:
            if cloud_cover > 80:
                analysis.append("Cloudy weather")
            elif cloud_cover < 20:
                analysis.append("Clear skies")
        
        if temp is not None and temp < -10 and wind_speed is not None and wind_speed > 20:
            analysis.append("Severe cold and windy, unfavorable for outdoor activities")
        
        if temp is not None and temp < 5 or wind_speed is not None and wind_speed > 20 or precipitation_prob > 70:
            analysis.append("Not ideal for outdoor sports or walks")
        
        if not analysis:
            analysis.append("Weather is mild and favorable")
        
        return analysis
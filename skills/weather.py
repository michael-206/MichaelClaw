import requests
import os
from dotenv import load_dotenv

load_dotenv()

weather_apikey = os.getenv("WEATHER_API_KEY")
# ----------------------------
# 1. Fake weather tool (replace with real API later)
# ----------------------------
def get_current_weather(location: str):
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_apikey}&q={location}&aqi=no").json()

    condidtion = response["current"]["condition"]["text"]
    temp = response["current"]["temp_c"]
    feels_like = response["current"]["feelslike_c"]
    precipitation = response["current"]["precip_mm"]


    return {
        "location": location,
        "temperature_c": temp,
        "condition": condidtion,
        "feels_like_c": feels_like,
        "percipitation_mm": precipitation
    }

def get_weather_forecast(location: str, days=3):
    response = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json"
        f"?key=318001503b194133a9a173251262104"
        f"&q={location}&days={days+1}&aqi=no&alerts=no"
    )

    data = response.json()

    # --- Current weather ---
    current = data.get("current", {})
    condition = current.get("condition", {}).get("text")
    temp = current.get("temp_c")
    feels_like = current.get("feelslike_c")
    precipitation = current.get("precip_mm")

    # --- Forecast ---
    forecast_list = []
    forecast_days = data.get("forecast", {}).get("forecastday", [])

    del forecast_days[0]

    for day in forecast_days:
        day_info = day.get("day", {})

        forecast_list.append({
            "date": day.get("date"),
            "min_temp_c": day_info.get("mintemp_c"),
            "max_temp_c": day_info.get("maxtemp_c"),
            "precipitation_mm": day_info.get("totalprecip_mm"),
            "condition": day_info.get("condition", {}).get("text")
        })

    # --- Final output ---
    output = {
        "current_weather": {
            "location": location,
            "temperature_c": temp,
            "condition": condition,
            "feels_like_c": feels_like,
            "precipitation_mm": precipitation
        },
        "forecast": forecast_list
    }

    return output
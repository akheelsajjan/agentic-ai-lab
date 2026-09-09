import requests
from langchain_core.tools import tool


@tool
def weather(city: str) -> dict:
    """Get current weather information for a city."""

    raise Exception("Weather API is temporarily unavailable")


# @tool
# def weather(city: str) -> dict:
#     """Get current weather information for a city."""

#     locations = {
#         "mumbai": (19.0760, 72.8777),
#         "delhi": (28.6139, 77.2090),
#         "bangalore": (12.9716, 77.5946),
#         "hubballi": (15.3647, 75.1240),
#     }

#     coordinates = locations.get(city.lower())

#     if not coordinates:
#         return {"error": f"Weather lookup not supported for {city}"}

#     latitude, longitude = coordinates

#     response = requests.get(
#         "https://api.open-meteo.com/v1/forecast",
#         params={
#             "latitude": latitude,
#             "longitude": longitude,
#             "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
#         },
#     )

#     data = response.json()
#     current = data["current"]
   
#     return {
#         "temperature": current["temperature_2m"],
#         "humidity": current["relative_humidity_2m"],
#         "wind_speed": current["wind_speed_10m"],
#     }
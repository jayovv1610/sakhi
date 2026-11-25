
import requests


def get_weather(city="Hyderabad"):
    """Get the current weather for a city."""

    try:
        # First, find the city's location
        location_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )

        location_response.raise_for_status()
        cities = location_response.json().get("results", [])

        if not cities:
            return "I couldn't find that city."

        city_info = cities[0]
        latitude = city_info["latitude"]
        longitude = city_info["longitude"]

        # Get the weather using the city's coordinates
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()
        weather = weather_response.json()["current"]

        temperature = weather["temperature_2m"]
        humidity = weather["relative_humidity_2m"]
        weather_code = weather["weather_code"]

        # Turn the weather code into a simple description
        if weather_code == 0:
            condition = "clear"
        elif weather_code in (1, 2):
            condition = "partly cloudy"
        elif weather_code == 3:
            condition = "overcast"
        elif weather_code in (45, 48):
            condition = "foggy"
        elif 51 <= weather_code <= 67:
            condition = "rainy"
        elif weather_code in (71, 73, 75, 77, 85, 86):
            condition = "snowy"
        elif 80 <= weather_code <= 82:
            condition = "rain showers"
        elif weather_code >= 95:
            condition = "thunderstorms"
        else:
            condition = "uncertain"

        # Give Sakhi a natural sentence to speak
        return (
            f"It's currently {temperature} degrees Celsius "
            f"in {city_info['name']}, with {condition} conditions "
            f"and {humidity} percent humidity."
        )

    except requests.RequestException:
        return "I couldn't retrieve the weather right now."

    except (KeyError, ValueError, TypeError):
        return "I couldn't understand the weather information."

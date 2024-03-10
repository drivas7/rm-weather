import json
import requests
import os
from config.config import WEATHER_API_URL, TEMPERATURE_PARAMS, RAIN_PARAMS

WEATHER_CODES_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "weather_codes.json")

def load_weather_codes(file_path):
    """Load weather codes from the specified JSON file.

    Args:
        file_path (str): Path to the JSON file containing the weather codes.

    Returns:
        dict: A dictionary containing weatheer codes.
    """
    try:
        with open(file_path) as f:
            weather_codes_list = json.load(f)
        return weather_codes_list
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON data from file '{file_path}'.")
        return None

# Load weather codes from the JSON file
weather_codes_list = load_weather_codes(WEATHER_CODES_FILE_PATH)


def get_weather_description(weather_code):
    return weather_codes_list.get(str(weather_code), "Unknown")

def get_temperature_forecast(city, latitude, longitude, timezone):
    """
    Fetches temperature forecast data from an API for the specified city.
    
    Args:
        city (string): City name.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (string): STD code of timezone.
    
    Returns:
        dict: Forecast data for the next 3 days.
    """
    try:
        # Fetch weather data from API
        if not WEATHER_API_URL:
            raise ValueError("WEATHER_API_URL environment variable is not set")

        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&timezone={timezone}&{TEMPERATURE_PARAMS}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        # The json returns data for the next 7 days. We want the data of 3 days from now.
        weather = data["daily"]
        # Parse weather data
        # forecast = {
        #     "city": city,
        #     "date": weather["time"][3],
        #     "timezone": timezone,
        #     "description": get_weather_description(weather["weather_code"][3]),
        #     "max_temperature": weather["temperature_2m_max"][3],
        #     "min_temperature": weather["temperature_2m_min"][3],
        #     "apparent_max_temperature": weather["apparent_temperature_max"][3],
        #     "apparent_min_temperature": weather["apparent_temperature_min"][3],
        #     "sunrise_time": weather["sunrise"][3],
        #     "sunset_time": weather["sunset"][3],
        # }
        # return forecast
    
        forecast = {}
    
        for i in range(4):
            date = weather["time"][i]
            # Construct weather information for the day
            day_forecast = {
                "city": city,
                "date": weather["time"][i],
                "timezone": timezone,
                "description": get_weather_description(weather["weather_code"][i]),
                "max_temperature": weather["temperature_2m_max"][i],
                "min_temperature": weather["temperature_2m_min"][i],
                "apparent_max_temperature": weather["apparent_temperature_max"][i],
                "apparent_min_temperature": weather["apparent_temperature_min"][i],
                "sunrise_time": weather["sunrise"][i],
                "sunset_time": weather["sunset"][i],
            }

            # Add day's forecast to the overall forecast dictionary
            forecast[date] = day_forecast
        
        return forecast
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected JSON structure: {e}")
        return None
    except ValueError as e:
        print(f"Environment variable error: {e}")
        return None


def get_rain_forecast(city, latitude, longitude, timezone):
    """
    Fetches rain forecast data from an API for the specified city.
    
    Args:
        city (string): City name.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (string): STD code of timezone.
    
    Returns:
        dict: Forecast data for the next 3 days.
    """
    try:
        # Fetch weather data from API
        if not WEATHER_API_URL:
            raise ValueError("WEATHER_API_URL environment variable is not set")

        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&timezone={timezone}&{RAIN_PARAMS}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        # The json returns data for the next 7 days. We want the data of 3 days from now.
        weather = data["daily"]

        # weather_code = weather["weather_code"][3]

        # if weather_code < 50 and weather_code not in [71, 73, 75, 77]:
        #     description = "No Rain - " + get_weather_description(weather_code)
        # else:
        #     description = get_weather_description(weather_code)

        # # Parse weather data
        # forecast = {
        #     "city": city,
        #     "date": weather["time"][3],
        #     "timezone": timezone,
        #     "description": description,
        #     "rain_sum_mm": weather["rain_sum"][3],
        #     "showers_sum_mm": weather["showers_sum"][3],
        #     "precipitation_probability_percentage": weather["precipitation_probability_max"][3],
        #     "wind_speed_max_kmh": weather["wind_speed_10m_max"][3]
        # }
        # return forecast

        forecast = {}
    
        for i in range(4):
            date = weather["time"][i]
            weather_code = weather["weather_code"][i]

            # Append "No Rain -" if weather code is not related to rain
            if weather_code < 50 and weather_code not in [71, 73, 75, 77]:
                description = "No Rain - " + get_weather_description(weather_code)
            else:
                description = get_weather_description(weather_code)

            # Construct weather information for the day
            day_forecast = {
                "city": city,
                "date": date,
                "timezone": timezone,
                "description": description,
                "rain_sum_mm": weather["rain_sum"][i],
                "showers_sum_mm": weather["showers_sum"][i],
                "precipitation_probability_percentage": weather["precipitation_probability_max"][i],
                "wind_speed_max_kmh": weather["wind_speed_10m_max"][i]
            }

            # Add day's forecast to the overall forecast dictionary
            forecast[date] = day_forecast
        
        return forecast
    
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected JSON structure: {e}")
        return None
    except ValueError as e:
        print(f"Environment variable error: {e}")
        return None
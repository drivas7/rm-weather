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

def get_temperature_forecast(city, latitude, longitude, timezone, days):
    """
    Fetches temperature forecast data from an API for the specified city.
    
    Args:
        city (string): City name.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (string): STD code of timezone.
        days (int): Number of days consulted.
    
    Returns:
        dict: Forecast data for the requested days.
    """
    try:
        # Fetch weather data from API
        if not WEATHER_API_URL:
            raise ValueError("WEATHER_API_URL environment variable is not set")
        if days > 16:
            raise IndexError("Days cannot be greater than 16.")
        
        # By default days = 0, and in this case it should return the data of 3 days from now
        i = 0
        j = i
        forecast_days = days

        if days == 0: 
            j = i + 3
            forecast_days = 4

        #url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&timezone={timezone}&{TEMPERATURE_PARAMS}&forecast_days={forecast_days}"

        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&{TEMPERATURE_PARAMS}&forecast_days={forecast_days}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        # The json returns data for the next 7 days. We want the data of 3 days from now.
        weather = data["daily"]
        # Parse weather data    

        forecast = {}
        
        days = days + 1
    
        for i in range(days):
            date = weather["time"][j]
            # Construct weather information for the day
            day_forecast = {
                "city": city,
                "date": weather["time"][j],
                "timezone": timezone,
                "description": get_weather_description(weather["weather_code"][j]),
                "max_temperature": str(weather["temperature_2m_max"][j]) + "°C",
                "min_temperature": str(weather["temperature_2m_min"][j]) + "°C",
                "apparent_max_temperature": str(weather["apparent_temperature_max"][j]) + "°C",
                "apparent_min_temperature": str(weather["apparent_temperature_min"][j]) + "°C",
                "sunrise_time": weather["sunrise"][j] + " GMT",
                "sunset_time": weather["sunset"][j] + " GMT",
            }
            # Add day's forecast to the overall forecast dictionary
            forecast[date] = day_forecast
            # This is needed because j determines which value is printed and i is the counter
            j = i 
        
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
    except IndexError as e:
        print(f"Parameter error: {e}")
        return None


def get_rain_forecast(city, latitude, longitude, timezone, days):
    """
    Fetches rain forecast data from an API for the specified city.
    
    Args:
        city (string): City name.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (string): STD code of timezone.
        days (int): Number of days consulted.
    
    Returns:
        dict: Forecast data for the requested days.
    """
    try:
        # Fetch weather data from API
        if not WEATHER_API_URL:
            raise ValueError("WEATHER_API_URL environment variable is not set")
        if days > 16:
            raise IndexError("Days cannot be greater than 16.")
        
        # By default days = 0, and in this case it should return the data of 3 days from now
        i = 0
        j = i
        forecast_days = days

        if days == 0: 
            j = i + 3
            forecast_days = 4
        
        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&timezone={timezone}&{RAIN_PARAMS}&forecast_days={forecast_days}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        weather = data["daily"]

        forecast = {}

        days = days + 1
    
        for i in range(days):
            date = weather["time"][j]
            weather_code = weather["weather_code"][j]

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
                "rain_sum": str(weather["rain_sum"][j]) + " mm",
                "showers_sum": str(weather["showers_sum"][j]) + " mm",
                "precipitation_probability": str(weather["precipitation_probability_max"][j]) + "%",
                "wind_speed_max": str(weather["wind_speed_10m_max"][j]) + " km/h"
            }
            j = i 
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
    except IndexError as e:
        print(f"Parameter error: {e}")
        return None
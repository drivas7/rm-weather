import os

WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
TEMPERATURE_PARAMS = os.environ.get("TEMPERATURE_PARAMS")
RAIN_PARAMS = os.environ.get("RAIN_PARAMS")
GEOLOCATION_API_URL = os.environ.get("GEOLOCATION_API_URL")

if not WEATHER_API_URL:
    raise ValueError("WEATHER_API_URL environment variable is not set")

if not TEMPERATURE_PARAMS:
    raise ValueError("TEMPERATURE_PARAMS environment variable is not set")

if not RAIN_PARAMS:
    raise ValueError("RAIN_PARAMS environment variable is not set")

if not GEOLOCATION_API_URL:
    raise ValueError("GEOLOCATION_API_URL environment variable is not set")
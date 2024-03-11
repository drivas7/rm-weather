import requests
from config.config import GEOLOCATION_API_URL


def get_city_information(city_name):
    """Get latitude, longitude, and timezone information for the specified city.

    Args:
        city_name (str): Name of the city.

    Returns:
        tuple: A tuple containing latitude, longitude, and timezone information.
    """
    
    cities_info_url = f"{GEOLOCATION_API_URL}{city_name}"

    response = requests.get(cities_info_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()

    try:
        city_info = data["results"][0]
        latitude = city_info["latitude"]
        longitude = city_info["longitude"]
        timezone = city_info["timezone"]
        if latitude is None or longitude is None or timezone is None:
            raise KeyError(f"Missing information for city '{city_name}'")
        return latitude, longitude, timezone
    
    except requests.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None
    except KeyError as e:
        print(f"Error: {e}")
        return None

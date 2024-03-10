import json
import os

# Define the path to the cities JSON file
CITIES_INFO_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cities.json")

def load_cities_data(file_path):
    """Load city information from the specified JSON file.

    Args:
        file_path (str): Path to the JSON file containing city information.

    Returns:
        dict: A dictionary containing city information.
    """
    try:
        with open(file_path) as f:
            cities_data = json.load(f)
        return cities_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON data from file '{file_path}'.")
        return None

# Load city information from the JSON file
cities = load_cities_data(CITIES_INFO_FILE_PATH)

def get_city_information(city_name):
    """Get latitude, longitude, and timezone information for the specified city.

    Args:
        city_name (str): Name of the city.

    Returns:
        tuple: A tuple containing latitude, longitude, and timezone information.
    """
    if cities is None:
        return None
    
    try:
        city_info = cities[city_name]
        latitude = city_info.get("latitude")
        longitude = city_info.get("longitude")
        timezone = city_info.get("timezone")
        if latitude is None or longitude is None or timezone is None:
            raise KeyError(f"Missing information for city '{city_name}'")
        return latitude, longitude, timezone
    except KeyError as e:
        print(f"Error: {e}")
        return None

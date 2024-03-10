from fastapi import FastAPI
from .weather import get_temperature_forecast, get_rain_forecast
from .cities import get_city_information

app = FastAPI()

@app.get("/temperature")
def get_temperature(city: str = "Lisbon"):
    """
    It accepts city as an optional parameter, 
    defaulting to Lisbon.

    """

    latitude, longitude, timezone = get_city_information(city)

    forecast = get_temperature_forecast(city, latitude, longitude, timezone)

    return forecast

@app.get("/rain")
def get_rain(city: str = "Lisbon"):
    """
    It accepts city as an optional parameter, 
    defaulting to Lisbon.

    """

    latitude, longitude, timezone = get_city_information(city)

    forecast = get_rain_forecast(city, latitude, longitude, timezone)
    return forecast
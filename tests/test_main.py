import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_temperature_forecast():
    response = client.get("/temperature?city=Lisbon")
    assert response.status_code == 200
    data = response.json()
    
    # Get the first date from the response data
    date = next(iter(data.keys()))  # Get the first key (date) from the response
    
    # Access data for the extracted date
    forecast_data = data[date]
    
    # Check if the required fields are present in the forecast data
    assert "city" in forecast_data
    assert "date" in forecast_data
    assert "timezone" in forecast_data
    assert "description" in forecast_data
    assert "max_temperature" in forecast_data
    assert "min_temperature" in forecast_data
    assert "apparent_max_temperature" in forecast_data
    assert "apparent_min_temperature" in forecast_data
    assert "sunrise_time" in forecast_data
    assert "sunset_time" in forecast_data


def test_get_rain_forecast():
    response = client.get("/rain?city=Lisbon")
    assert response.status_code == 200
    data = response.json()
        
    # Get the first date from the response data
    date = next(iter(data.keys()))  # Get the first key (date) from the response
    
    # Access data for the extracted date
    forecast_data = data[date]
    
    # Check if the required fields are present in the forecast data
    assert "city" in forecast_data
    assert "date" in forecast_data
    assert "timezone" in forecast_data
    assert "description" in forecast_data
    assert "rain_sum" in forecast_data
    assert "showers_sum" in forecast_data
    assert "precipitation_probability" in forecast_data
    assert "wind_speed_max" in forecast_data

# Test performance
@pytest.mark.benchmark(group="performance")
def test_temperature_forecast_performance(benchmark):
    # Benchmark the temperature forecast endpoint
    result = benchmark(client.get, "/temperature?city=Lisbon")
    assert result.status_code == 200

@pytest.mark.benchmark(group="performance")
def test_rain_forecast_performance(benchmark):
    # Benchmark the rain forecast endpoint
    result = benchmark(client.get, "/rain?city=Lisbon")
    assert result.status_code == 200
import pytest
import requests
from unittest.mock import patch
from prod_aplikacja.data_fetcher import fetch_station, fetch_sensor, fetch_measurement

# Mock data
mock_station_data = [
    {'id': 1, 'stationName': 'Station 1', 'gegrLat': 52.229675, 'gegrLon': 21.012230, 'city': {'id': 1}},
    {'id': 2, 'stationName': 'Station 2', 'gegrLat': 50.064650, 'gegrLon': 19.944980, 'city': {'id': 2}},
]

mock_sensor_data = [
    {'id': 101, 'stationId': 1, 'param': {'paramName': 'PM10', 'paramFormula': 'PM10', 'paramCode': 'PM10', 'idParam': 1}},
    {'id': 102, 'stationId': 1, 'param': {'paramName': 'PM2.5', 'paramFormula': 'PM2.5', 'paramCode': 'PM25', 'idParam': 2}},
]

mock_measurement_data = {
    'values': [
        {'date': '2024-01-01 00:00:00', 'value': 10.0},
        {'date': '2024-01-01 01:00:00', 'value': 20.0},
    ]
}

# Test for fetch_station
@patch('prod_aplikacja.data_fetcher.requests.get')
def test_fetch_station(mock_get):
    """Test for the fetch_station function."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_station_data

    stations = fetch_station()
    assert len(stations) == 2
    assert stations[0]['stationName'] == 'Station 1'
    mock_get.assert_called_once_with("https://powietrze.gios.gov.pl/pjp-api/rest/station/findAll")

# Test for fetch_sensor
@patch('prod_aplikacja.data_fetcher.requests.get')
def test_fetch_sensor(mock_get):
    """Test for the fetch_sensor function."""
    station_id = 1
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_sensor_data

    sensors = fetch_sensor(station_id)
    assert len(sensors) == 2
    assert sensors[0]['param']['paramName'] == 'PM10'
    mock_get.assert_called_once_with(f"https://powietrze.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}")

# Test for fetch_measurement
@patch('prod_aplikacja.data_fetcher.requests.get')
def test_fetch_measurement(mock_get):
    """Test for the fetch_measurement function."""
    sensor_id = 101
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_measurement_data

    measurements = fetch_measurement(sensor_id)
    assert len(measurements['values']) == 2
    assert measurements['values'][0]['value'] == 10.0
    mock_get.assert_called_once_with(f"https://powietrze.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}")

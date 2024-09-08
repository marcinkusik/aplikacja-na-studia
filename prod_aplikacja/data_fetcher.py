import requests

def fetch_station():
    """
    Fetches all air quality monitoring stations data from the API.

    Sends a GET request to the API to retrieve data about all available stations.

    Returns:
    list: A list of dictionaries containing station data if the request is successful.

    Raises:
    Exception: If the request fails or returns a status code other than 200.
    """
    url = "https://powietrze.gios.gov.pl/pjp-api/rest/station/findAll"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch station data")

def fetch_sensor(station_id):
    """
    Fetches sensor data for a specific station from the API.

    Sends a GET request to retrieve the list of sensors for a given station.

    Parameters:
    station_id (int): The ID of the station for which to fetch the sensors.

    Returns:
    list: A list of dictionaries containing sensor data if the request is successful.

    Raises:
    Exception: If the request fails or returns a status code other than 200.
    """
    url = f"https://powietrze.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch sensor data")

def fetch_measurement(sensor_id):
    """
    Fetches measurement data for a specific sensor from the API.

    Sends a GET request to retrieve the measurement data for a given sensor.

    Parameters:
    sensor_id (int): The ID of the sensor for which to fetch the measurements.

    Returns:
    dict: A dictionary containing the measurement data if the request is successful.

    Raises:
    Exception: If the request fails or returns a status code other than 200.
    """
    url = f"https://powietrze.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch measurement data")

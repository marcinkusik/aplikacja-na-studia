import pytest
import sqlite3
from prod_aplikacja.database_manager import DatabaseManager


@pytest.fixture
def db_manager():
    """
    Fixture to create an instance of DatabaseManager with an in-memory SQLite database.
    This ensures the tests are isolated and do not affect the actual database.
    """
    db_manager = DatabaseManager(':memory:')  # Use an in-memory database for testing
    return db_manager


def test_create_tables(db_manager):
    """
    Test to check if tables are created successfully in the database.
    """
    tables = db_manager.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    table_names = [table[0] for table in tables]

    assert 'stations' in table_names
    assert 'sensors' in table_names
    assert 'measurements' in table_names
    assert 'air_quality_index' in table_names


def test_insert_station(db_manager):
    """
    Test for inserting a station into the 'stations' table.
    """
    station_data = (1, 'Station 1', 52.229675, 21.012230, 1, 'Street 1')
    db_manager.insert_station(station_data)

    stations = db_manager.fetch_stations()
    assert len(stations) == 1
    assert stations[0][1] == 'Station 1'


def test_insert_sensors(db_manager):
    """
    Test for inserting sensors into the 'sensors' table.
    """
    sensor_data = [
        {'id': 101, 'stationId': 1,
         'param': {'paramName': 'PM10', 'paramFormula': 'PM10', 'paramCode': 'PM10', 'idParam': 1}},
        {'id': 102, 'stationId': 1,
         'param': {'paramName': 'PM2.5', 'paramFormula': 'PM2.5', 'paramCode': 'PM25', 'idParam': 2}},
    ]

    db_manager.insert_sensors(sensor_data)
    sensors = db_manager.fetch_sensors(1)
    assert len(sensors) == 2
    assert sensors[0][2] == 'PM10'
    assert sensors[1][2] == 'PM2.5'


def test_insert_measurements(db_manager):
    """
    Test for inserting measurements into the 'measurements' table.
    """
    measurement_data = {
        'values': [
            {'date': '2024-01-01 00:00:00', 'value': 10.0},
            {'date': '2024-01-01 01:00:00', 'value': 20.0},
        ]
    }

    db_manager.insert_measurements(measurement_data, 101)
    measurements = db_manager.fetch_measurements(101)
    assert len(measurements) == 2
    assert measurements[0][2] == '2024-01-01 00:00:00'
    assert measurements[0][3] == 10.0


def test_insert_air_quality_index(db_manager):
    """
    Test for inserting air quality index data into the 'air_quality_index' table.
    """
    index_data = (1, 1, '2024-01-01 00:00:00', 1, 'Good', '2024-01-01 00:00:00')

    db_manager.insert_air_quality_index(index_data)
    air_quality_index = db_manager.fetch_air_quality_index(1)
    assert len(air_quality_index) == 1
    assert air_quality_index[0][4] == 'Good'

import pytest
from prod_aplikacja.data_analyzer import Analyze_Data

# Sample data for testing
sample_data = [
    {'id': 1, 'station_id': 101, 'timestamp': '2024-01-01 00:00:00', 'value': 10.0},
    {'id': 2, 'station_id': 101, 'timestamp': '2024-01-01 01:00:00', 'value': 20.0},
    {'id': 3, 'station_id': 101, 'timestamp': '2024-01-01 02:00:00', 'value': 30.0},
    {'id': 4, 'station_id': 101, 'timestamp': '2024-01-01 03:00:00', 'value': 40.0},
    {'id': 5, 'station_id': 101, 'timestamp': '2024-01-01 04:00:00', 'value': 50.0},
]


@pytest.fixture
def analyzer():
    """
    Fixture to create an instance of Analyze_Data with sample data.

    Returns:
    Analyze_Data: Instance of the class initialized with sample data.
    """
    return Analyze_Data(sample_data)


def test_min_value(analyzer):
    """
    Test for the min_value method.
    Ensures that the minimum value is correctly calculated.
    """
    assert analyzer.min_value('value') == 10.0


def test_max_value(analyzer):
    """
    Test for the max_value method.
    Ensures that the maximum value is correctly calculated.
    """
    assert analyzer.max_value('value') == 50.0


def test_mean_value(analyzer):
    """
    Test for the mean_value method.
    Ensures that the mean value is correctly calculated.
    """
    assert analyzer.mean_value('value') == pytest.approx(30.0)


def test_trend(analyzer):
    """
    Test for the trend method.
    Ensures that the trend (average difference between consecutive values) is correctly calculated.
    """
    expected_trend = (20.0 - 10.0 + 30.0 - 20.0 + 40.0 - 30.0 + 50.0 - 40.0) / 4
    assert analyzer.trend('value') == pytest.approx(expected_trend)

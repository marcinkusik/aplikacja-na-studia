import pytest
import pandas as pd
from unittest.mock import patch
from prod_aplikacja.data_visualizer import Visualize_data
import matplotlib.pyplot as plt

# Mock data for testing
mock_data = [
    {'station_id': 1, 'sensor_id': 101, 'date': '2024-01-01', 'value': 10.0},
    {'station_id': 1, 'sensor_id': 101, 'date': '2024-01-02', 'value': 20.0},
    {'station_id': 1, 'sensor_id': 101, 'date': '2024-01-03', 'value': 30.0},
    {'station_id': 1, 'sensor_id': 101, 'date': '2024-01-04', 'value': 40.0},
    {'station_id': 1, 'sensor_id': 101, 'date': '2024-01-05', 'value': 50.0},
]


@pytest.fixture
def visualizer():
    """Fixture to create an instance of Visualize_data with mock data."""
    return Visualize_data(mock_data)


@patch('visualize_data.plt.show')
def test_plot_data(mock_show, visualizer):
    """
    Test for the plot_data method.
    This test checks whether the plotting function is called correctly without errors.
    """
    with patch('data_visualizer.plot_data.plt.plot') as mock_plot, patch('data_visualizer.data_visualizer.plot_data.plt.xticks') as mock_xticks:
        visualizer.plot_data('value')

        # Ensure that plt.plot and plt.show were called
        mock_plot.assert_called_once_with(visualizer.data['date'], visualizer.data['value'])
        mock_xticks.assert_called_once_with(visualizer.data['date'][::5], rotation=90)
        mock_show.assert_called_once()


def test_missing_data(visualizer):
    """
    Test for plot_data method when data is missing.
    Ensures the function handles missing data gracefully.
    """
    # Remove the 'date' column to simulate missing data
    visualizer.data.drop(columns=['date'], inplace=True)

    with patch('builtins.print') as mock_print:
        visualizer.plot_data('value')
        mock_print.assert_called_once_with("Error: Data missing from source.")

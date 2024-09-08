import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as md


class Visualize_data:
    """
    A class used to visualize air quality data by creating plots of sensor measurements over time.
    """
    def __init__(self, data):
        """
        Initializes the Visualize_data class by creating a pandas DataFrame from the input data.

        Parameters:
        data (list or DataFrame): A list of dictionaries or a DataFrame containing the air quality data.
                                  If a list is provided, it is converted into a DataFrame.
        """
        # Create dataframe
        if isinstance(data, list):
            self.data = pd.DataFrame(data)
        else:
            self.data = data

        # Names for columns
        if len(self.data.columns) == 4:
            self.data.columns = ['station_id', 'sensor_id', 'date', 'value']

    def plot_data(self, param):
        """
        Plots the specified parameter from the dataset over time.

        Parameters:
        param (str): The name of the column to plot (typically 'value').

        Returns:
        None: Displays the plot but does not return any value.
        """
        # Check data structure
        if 'date' not in self.data or param not in self.data:
            print("Error: Data missing from source.")
            return

        # Create a graph
        plt.plot(self.data['date'], self.data[param])

        # Title for axes and graph
        plt.xlabel('Date')  # X axis
        plt.ylabel('Value')  # Y axis
        plt.title('Graph')  # Title of graph

        # Date formatting
        plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
        # plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d %H:%M')) #includes hourly data
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d')) #without hourly data

        # View every 5th data point on the x-axis
        plt.xticks(self.data['date'][::5], rotation=90)

        # View graph
        plt.tight_layout()  # Poprawa układu wykresu
        plt.show()

import pandas as pd

class Analyze_Data:
    """
    A class used to analyze air quality data including finding minimum, maximum,
    mean values, and determining the trend.
    """
    def __init__(self, data):
        """
        Initializes the Analyze_Data class by converting input data into a pandas DataFrame.

        Parameters:
        data (list): A list of dictionaries or records containing data with 'id', 'station_id',
                     'timestamp', and 'value' columns.
        """
        self.data = pd.DataFrame(data, columns=['id', 'station_id', 'timestamp', 'value'])

    def min_value(self, param):
        """
        Returns the minimum value for the specified column.

        Parameters:
        param (str): The name of the column to calculate the minimum value for.

        Returns:
        float: The minimum value in the specified column.
        """
        return self.data[param].min()

    def max_value(self, param):
        """
        Returns the maximum value for the specified column.

        Parameters:
        param (str): The name of the column to calculate the maximum value for.

        Returns:
        float: The maximum value in the specified column.
        """
        return self.data[param].max()

    def mean_value(self, param):
        """
        Returns the mean value for the specified column.

        Parameters:
        param (str): The name of the column to calculate the mean value for.

        Returns:
        float: The mean value in the specified column.
        """
        return self.data[param].mean()

    def trend(self, param):
        """
        Returns the average change (trend) between consecutive values in the specified column.

        Parameters:
        param (str): The name of the column to calculate the trend for.

        Returns:
        float: The average difference between consecutive values in the specified column.
        """
        return self.data[param].diff().mean()

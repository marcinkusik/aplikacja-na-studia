import tkinter as tk
from tkinter import ttk, messagebox, font
from database_manager import DatabaseManager
from data_fetcher import fetch_station, fetch_sensor, fetch_measurement
from data_analyzer import Analyze_Data
from data_visualizer import Visualize_data


class AirQualityMonitorApp:
    """
    A GUI application class for monitoring air quality data, allowing the user to load stations, sensors,
    download data, analyze data, and visualize it in a chart.
    """
    def __init__(self, root):
        """
        Initializes the AirQualityMonitorApp class by setting up the GUI and connecting to the database.

        Parameters:
        root (Tk): The main root window for the tkinter application.
        """
        self.root = root
        self.root.title("Air Quality Monitor")

        # Font settings
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=15, weight="bold", underline=True, family="Helvetica")
        self.root.option_add("*Font", default_font)

        self.db_manager = DatabaseManager()

        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the graphical user interface, including dropdowns and buttons for stations, sensors,
        data downloading, analysis, and plotting.
        """
        # Stations
        self.station_label = ttk.Label(self.root, text="Select a station:")
        self.station_label.pack(padx=10, pady=5, anchor='w')

        self.station_combobox = ttk.Combobox(self.root)
        self.station_combobox.pack(padx=10, pady=5, fill='x')

        self.load_stations_button = ttk.Button(self.root, text="Load stations", command=self.load_stations)
        self.load_stations_button.pack(padx=10, pady=5, anchor='w')

        # Sensors
        self.sensor_label = ttk.Label(self.root, text="Select a sensor:")
        self.sensor_label.pack(padx=10, pady=5, anchor='w')

        self.sensor_combobox = ttk.Combobox(self.root)
        self.sensor_combobox.pack(padx=10, pady=5, fill='x')

        self.load_sensors_button = ttk.Button(self.root, text="Load sensors", command=self.load_sensors)
        self.load_sensors_button.pack(padx=10, pady=5, anchor='w')

        # Download button
        self.load_data_button = ttk.Button(self.root, text="Download data", command=self.load_data)
        self.load_data_button.pack(padx=10, pady=5, anchor='w')

        # Analyze button
        self.analyze_data_button = ttk.Button(self.root, text="Analyze data", command=self.analyze_data)
        self.analyze_data_button.pack(padx=10, pady=5, anchor='w')

        # Button to create a graph
        self.plot_data_button = ttk.Button(self.root, text="Draw a chart", command=self.plot_data)
        self.plot_data_button.pack(padx=10, pady=5, anchor='w')

    def load_stations(self):
        """
        Loads the available stations from the API and stores them in the database.
        Populates the station dropdown list in the GUI.
        """
        try:
            stations = fetch_station()
            for station in stations:
                station_data = (
                    station['id'], station['stationName'], station['gegrLat'], station['gegrLon'],
                    station['city']['id'],
                    station.get('addressStreet', ''))
                self.db_manager.insert_station(station_data)
            self.station_combobox['values'] = [station['stationName'] for station in stations]
            messagebox.showinfo("Information", "Stations have been loaded.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def load_sensors(self):
        """
        Loads the available sensors for the selected station from the API and stores them in the database.
        Populates the sensor dropdown list in the GUI.
        """
        try:
            station_name = self.station_combobox.get()
            station_id = self.get_station_id_by_name(station_name)
            if station_id:
                sensors = fetch_sensor(station_id)
                for sensor in sensors:
                    self.db_manager.insert_sensors([sensor])
                self.sensor_combobox['values'] = [sensor['param']['paramName'] for sensor in sensors]
                messagebox.showinfo("Information", "Sensors have been loaded.")
            else:
                messagebox.showerror("Error!", "Select a station.")
        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def load_data(self):
        """
        Downloads measurement data for the selected sensor from the API and stores it in the database.
        """
        try:
            sensor_name = self.sensor_combobox.get()
            sensor_id = self.get_sensor_id_by_name(sensor_name)
            if sensor_id:
                measurements = fetch_measurement(sensor_id)
                self.db_manager.insert_measurements(measurements, sensor_id)
                messagebox.showinfo("Information", "Data has been downloaded and saved in the database.")
            else:
                messagebox.showerror("Error!", "Select a sensor.")
        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def analyze_data(self):
        """
        Analyzes the data for the selected sensor, including calculating the minimum, maximum,
        mean values, and trend. Displays the results in a messagebox.
        """
        try:
            sensor_name = self.sensor_combobox.get()
            sensor_id = self.get_sensor_id_by_name(sensor_name)
            if sensor_id:
                measurements = self.db_manager.fetch_measurements(sensor_id)
                analyzer = Analyze_Data(measurements)
                min_val = analyzer.min_value('value')
                max_val = analyzer.max_value('value')
                mean_val = analyzer.mean_value('value')
                trend = analyzer.trend('value')
                messagebox.showinfo("Analyze data",
                                    f"Min: {min_val}\nMax: {max_val}\nMean: {mean_val}\nTrend: {trend}")
            else:
                messagebox.showerror("Error!", "Select a sensor.")
        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def plot_data(self):
        """
        Plots the measurement data for the selected sensor using matplotlib.
        """
        try:
            sensor_name = self.sensor_combobox.get()
            sensor_id = self.get_sensor_id_by_name(sensor_name)
            if sensor_id:
                measurements = self.db_manager.fetch_measurements(sensor_id)
                visualizer = Visualize_data(measurements)
                visualizer.plot_data('value')
            else:
                messagebox.showerror("Error!", "Select a sensor.")
        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def get_station_id_by_name(self, station_name):
        """
        Retrieves the station ID for a given station name from the database.

        Parameters:
        station_name (str): The name of the station to search for.

        Returns:
        int: The ID of the station, or None if not found.
        """
        stations = self.db_manager.fetch_stations()
        for station in stations:
            if station[1] == station_name:
                return station[0]
        return None

    def get_sensor_id_by_name(self, sensor_name):
        """
        Retrieves the sensor ID for a given sensor name from the database.

        Parameters:
        sensor_name (str): The name of the sensor to search for.

        Returns:
        int: The ID of the sensor, or None if not found.
        """
        station_name = self.station_combobox.get()
        station_id = self.get_station_id_by_name(station_name)
        sensors = self.db_manager.fetch_sensors(station_id)
        for sensor in sensors:
            if sensor[2] == sensor_name:
                return sensor[0]
        return None


def run_gui():
    """
    Initializes and runs the tkinter graphical user interface.
    """
    root = tk.Tk()
    root.geometry("400x600")  # Window size
    app = AirQualityMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
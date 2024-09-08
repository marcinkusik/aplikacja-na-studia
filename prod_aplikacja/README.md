Air Quality Monitor Application

This is a Python application with a gui built using Tkinter, 
designed to monitor air quality by fetching data from external APIs. 
The application allows users to load stations, select sensors, 
download air quality measurements, analyze the data, and visualize it in charts.

Features:

Load Stations: Fetches a list of air quality monitoring stations from 
an external API and stores them in a local SQLite database.

Load Sensors: After selecting a station, the application loads 
the available sensors and stores them in the database.

Download Data: Fetches measurement data for the selected sensor and stores it in the database.

Analyze Data: Calculates the minimum, maximum, average values, and trend of the downloaded data.

Visualize Data: Plots a chart showing the sensor measurements over time.

Prerequisites:

- Python 3.8+
- Tkinter (usually comes pre-installed with Python)
- SQLite (comes built-in with Python)

The following Python packages:
- requests
- matplotlib
- pandas

You can install packages by command:
pip3 install -r requirements.txt

Clone repo:
git clone git@github.com:marcinkusik/aplikacja-na-studia.git

Usage
Load Stations: Click "Load stations" to fetch a list of air quality monitoring stations from the API. 
The stations will be displayed in the station dropdown list.

Select a Station: Choose a station from the dropdown list.

Load Sensors: After selecting a station, click "Load sensors" to fetch and display available sensors for that station.

Download Data: Select a sensor from the dropdown list and click "Download data" to fetch air quality measurements 
from the API.

Analyze Data: Click "Analyze data" to calculate the minimum, maximum, average values, and trend for the selected sensor.

Visualize Data: Click "Draw a chart" to generate a chart displaying sensor measurements over time.
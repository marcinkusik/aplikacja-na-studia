import sqlite3

class DatabaseManager:
    """
    A class to manage the air quality database.
    """
    def __init__(self, db_name='air_quality.db'):
        """
        Initializes the DatabaseManager class.
        Parameters:
            db_name (str): The name of the database.
        """
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Creates necessary tables in the database for stations, sensors, measurements, and air quality index data.
        If the tables already exist, they will not be recreated.
        """
        c = self.conn.cursor()

########################################################################
#################SECTION THAT CREATES TABLES############################
########################################################################

        # 'stations' table
        c.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY,
            stationName TEXT,
            gegrLat REAL,
            gegrLon REAL,
            cityId INTEGER,
            addressStreet TEXT
        )
        ''')

        # 'sensors' table
        c.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY,
            stationId INTEGER,
            paramName TEXT,
            paramFormula TEXT,
            paramCode TEXT,
            idParam INTEGER,
            FOREIGN KEY(stationId) REFERENCES stations(id)
        )
        ''')

        # 'measurements' table
        c.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY,
            sensorId INTEGER,
            date TEXT,
            value REAL,
            FOREIGN KEY(sensorId) REFERENCES sensors(id)
        )
        ''')

        # 'air_quality_index' table
        c.execute('''
        CREATE TABLE IF NOT EXISTS air_quality_index (
            id INTEGER PRIMARY KEY,
            stationId INTEGER,
            stCalcDate TEXT,
            stIndexLevel INTEGER,
            indexLevelName TEXT,
            stSourceDataDate TEXT,
            FOREIGN KEY(stationId) REFERENCES stations(id)
        )
        ''')

        # commit changes
        self.conn.commit()

########################################################################
#################SECTION THAT INSERTS DATA##############################
########################################################################

    def insert_station(self, station_data):
        """
        Inserts a new station record into the 'stations' table if it does not already exist.

        Parameters:
        station_data (tuple): A tuple containing the station data.
        """
        c = self.conn.cursor()
        c.execute('''
        INSERT OR IGNORE INTO stations (id, stationName, gegrLat, gegrLon, cityId, addressStreet)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', station_data)
        self.conn.commit()

    def insert_sensors(self, sensors):
        """
        Inserts new sensor records into the 'sensors' table if they do not already exist.

        Parameters:
        sensors (list): A list of dictionaries containing sensor data.
        """
        c = self.conn.cursor()
        for sensor in sensors:
            c.execute('''
            INSERT OR IGNORE INTO sensors (id, stationId, paramName, paramFormula, paramCode, idParam)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (sensor['id'], sensor['stationId'], sensor['param']['paramName'], sensor['param']['paramFormula'], sensor['param']['paramCode'], sensor['param']['idParam']))
        self.conn.commit()

    def insert_measurements(self, measurements, sensor_id):
        """
        Inserts new measurement records into the 'measurements' table if they do not already exist.

        Parameters:
        measurements (dict): A dictionary containing measurement data.
        sensor_id (int): The ID of the sensor to which the measurements belong.
        """
        c = self.conn.cursor()
        for measurement in measurements['values']:
            c.execute('''
            INSERT OR IGNORE INTO measurements (sensorId, date, value)
            VALUES (?, ?, ?)
            ''', (sensor_id, measurement['date'], measurement['value']))
        self.conn.commit()

    def insert_air_quality_index(self, index_data):
        """
        Inserts a new air quality index record into the 'air_quality_index' table if it does not already exist.

        Parameters:
        index_data (tuple): A tuple containing the air quality index data (id, stationId, stCalcDate, stIndexLevel, indexLevelName, stSourceDataDate).
        """
        c = self.conn.cursor()
        c.execute('''
        INSERT OR IGNORE INTO air_quality_index (id, stationId, stCalcDate, stIndexLevel, indexLevelName, stSourceDataDate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', index_data)
        self.conn.commit()

########################################################################
#################SECTION THAT DOWNLOADS DATA############################
########################################################################

    def fetch_stations(self):
        """
        Fetches all station records from the 'stations' table and returns them.

        Returns:
        list: A list of tuples, where each tuple contains a station record.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM stations ORDER BY stationName ASC")
        stations = c.fetchall()
        return stations

    def fetch_sensors(self, station_id):
        """
        Fetches all sensor records for a given station ID from the 'sensors' table.

        Parameters:
        station_id (int): The ID of the station for which to fetch sensors.

        Returns:
        list: A list of tuples, where each tuple contains a sensor record.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM sensors WHERE stationId=?", (station_id,))
        return c.fetchall()

    def fetch_measurements(self, sensor_id):
        """
        Fetches all measurement records for a given sensor ID from the 'measurements' table.

        Parameters:
        sensor_id (int): The ID of the sensor for which to fetch measurements.

        Returns:
        list: A list of tuples, where each tuple contains a measurement record.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM measurements WHERE sensorId=?", (sensor_id,))
        return c.fetchall()

    def fetch_air_quality_index(self, station_id):
        """
        Fetches the air quality index records for a given station ID from the 'air_quality_index' table.

        Parameters:
        station_id (int): The ID of the station for which to fetch air quality index data.

        Returns:
        list: A list of tuples, where each tuple contains an air quality index record.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM air_quality_index WHERE stationId=?", (station_id,))
        return c.fetchall()

    def close_connection(self):
        """
        Closes the connection to the SQLite database.
        """
        self.conn.close()
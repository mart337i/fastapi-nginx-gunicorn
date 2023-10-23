# Module Imports
import mariadb
import sys

class MariaDB:

    #NOTE:: Better to set the information from a hidden .env file
    dbname = 'facility'

    def __init__(self):
        self.setup()  # Automatically call setup when an instance is created

    def get_curser(self):
        try:
            print("Starting connection atempt")
            conn = mariadb.connect(
                user="pi",
                password="Vds79bzw-",
                host="localhost",
                port=3306,
                database=self.dbname
            )
            print(f"connection : {conn}")
            return conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(-1)



    def execute(self,cursor,query):
        """
            Method to exacute any query.
            *self
            *curser db curser 
            *query 
            
        """
        try:
            cursor.execute(query)
        except mariadb.Error as e:
            print(f"Error: {e}")

    def setup(self):
        """ Init method for init query
        
        """
        _cr = self.get_curser()
        print(_cr.connection)  # Fixed this line by printing _cr.connection instead of res.connection
        res = self.execute(_cr,self.init_query())
        print(res)


    def init_query (self):
        return f"""
            USE {self.dbname}; 
            -- Facility table
            CREATE TABLE Facility (
                id INT PRIMARY KEY AUTO_INCREMENT,
                beskrivelse CHAR
            );

            -- Building table
            CREATE TABLE Building (
                id INT PRIMARY KEY,
                name CHAR,
                Facility_id INT,
                FOREIGN KEY (Facility_id) REFERENCES Facility(id)
            );

            -- Alarm table
            CREATE TABLE Alarm (
                id INT PRIMARY KEY AUTO_INCREMENT,
                type ENUM('warning','failure'),
                sonor_id INT
                -- Add foreign key constraints if required
            );

            -- Pollution sensor table
            CREATE TABLE PollutionSensor (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name CHAR,
                value DECIMAL,
                datetime DATETIME,
                building_id INT,
                FOREIGN KEY (building_id) REFERENCES Building(id)
            );

            -- Temperature and humidity sensor table
            CREATE TABLE TemperatureHumiditySensor (
                id INT PRIMARY KEY AUTO_INCREMENT,
                type ENUM('warning','failure','good','low'),
                value DECIMAL,
                name CHAR,
                datetime DATETIME,
                building_id INT,
                FOREIGN KEY (building_id) REFERENCES Building(id)
            );

        """
# Module Imports
import mariadb
import sys

class MariaDB:
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
                database="facility"
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


    def innit_query ():
        return """
            USE facility; 
            CREATE TABLE facility (
                ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                DESC CHAR,
            );
            CREATE TABLE building (
                ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            ) ;
            CREATE TABLE pollution_sensor (
                ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            
            );
            CREATE TABLE temperature_humidity_sensor (
                ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            
            );

        """
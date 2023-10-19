# Module Imports
import mariadb
import sys

class MariaDB():
    __name__ = "Maria Db"
    __description__ = "Maria db connection"


    def get_curser(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user="db_user",
                password="db_user_passwd",
                host="192.0.2.1",
                port=3306,
                database="employees"
            )
            # Get Cursor
            return conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(-1)

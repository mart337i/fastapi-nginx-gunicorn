

from typing import Union

from pydantic import BaseModel


class Facility(BaseModel):
    id: int
    desc: chr

    def insert_into_facility(self,value):
        return f"""
            INSERT INTO Facility (Description) VALUES ('{value}');
        """
    
    def get_facility(self):
        return """
            SELECT * FROM Facility;
        """

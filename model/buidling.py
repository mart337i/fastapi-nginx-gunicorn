

from typing import Union

from pydantic import BaseModel


class Building(BaseModel):
    id: int
    name: str
    facility_id : int

    def insert_into_building(self,values):
        return f"""
            INSERT INTO Building (name, Facility_id) VALUES ('{values['name']}', {values['Facility_id']});
        """
    
    def get_building(self):
        return """
            SELECT * FROM Building;
        """


from typing import Union
import datetime

from pydantic import BaseModel


class PollutionSensor(BaseModel):
    id: int
    name: chr
    value:float
    value_updated : datetime
    building_id : int

    def insert_into_pollution_sensor(self,values):
        return f"""
            INSERT INTO Alarm (type, sonor_id) VALUES ('{values['type']}', {values['sonor_id']});
        """
    
        
    def get_temperature_pollution_sensor(self):
        return """
            SELECT * FROM PollutionSensor;
        """
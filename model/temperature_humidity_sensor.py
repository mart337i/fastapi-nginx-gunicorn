

from typing import Union
import datetime

from pydantic import BaseModel


class TemperatureHumiditySensor():
    id: int
    name: str
    type: enumerate # In the DB its an Enum   
    value: float
    value_taken: datetime
    building_id : int

    def insert_into_temperature_humidity_sensor(self,values):
        return f"""
            INSERT INTO TemperatureHumiditySensor (type, value, name, datetime, building_id) VALUES ('{values['type']}', {values['value']}, '{values['name']}', '{datetime.datetime.today()}', {values['building_id']});
        """
    
    def get_temperature_humidity_sensor(self):
        return """
            SELECT * FROM TemperatureHumiditySensor;
        """
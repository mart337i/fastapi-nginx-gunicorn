
from typing import Union

from pydantic import BaseModel


class Alarm(BaseModel):
    id : int 
    type : enumerate
    senor_id : int

    def new_alarm(self,values):
        return f"""
            INSERT INTO Alarm (type, sonor_id) VALUES ('{values['type']}', {values['sensor_id']});
        """
    
    def get_alarm(self):
        return """
            SELECT * FROM Alarm;
        """
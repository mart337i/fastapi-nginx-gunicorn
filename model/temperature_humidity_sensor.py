

from typing import Union
import datetime

from pydantic import BaseModel


class TemperatureHumiditySensor(BaseModel):
    id: int
    name: chr
    type: chr # In the DB its an Enum   
    value: float
    value_taken: datetime
    building_id : int

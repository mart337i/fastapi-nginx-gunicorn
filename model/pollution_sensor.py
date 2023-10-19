

from typing import Union
import datetime

from pydantic import BaseModel


class PollutionSensor(BaseModel):
    id: int
    name: chr
    value:float
    value_updated : datetime
    building_id : int

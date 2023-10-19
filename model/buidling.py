

from typing import Union

from pydantic import BaseModel


class Building(BaseModel):
    id: int
    name: chr
    facility_id : int
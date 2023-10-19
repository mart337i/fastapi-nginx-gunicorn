

from typing import Union

from pydantic import BaseModel


class Facility(BaseModel):
    id: int
    desc: chr
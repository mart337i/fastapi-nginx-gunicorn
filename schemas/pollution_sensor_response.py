from pydantic import BaseModel

class PollutionSensorResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

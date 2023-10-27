from pydantic import BaseModel

class AlarmResponse(BaseModel):
    id: int
    type: str
    sonor_id : int

    class Config:
        orm_mode = True

from pydantic import BaseModel

class AlarmResponse(BaseModel):
    id: int
    type: str

    class Config:
        orm_mode = True

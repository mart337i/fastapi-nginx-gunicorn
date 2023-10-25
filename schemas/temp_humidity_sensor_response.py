from pydantic import BaseModel

class TempHumiditySensorResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True

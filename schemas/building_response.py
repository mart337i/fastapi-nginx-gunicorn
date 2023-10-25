from pydantic import BaseModel

class BuildingResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

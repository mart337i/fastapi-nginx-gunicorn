from pydantic import BaseModel

class FacilityResponse(BaseModel):
    id: int
    beskrivelse: str

    class Config:
        orm_mode = True

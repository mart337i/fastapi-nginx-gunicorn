from fastapi import APIRouter, HTTPException
from models.facility import Facility
from schemas.facility_response import FacilityResponse  # Import the response schema
from pydantic import BaseModel  # Import BaseModel from Pydantic

router = APIRouter()

class FacilityCreate(BaseModel):
    beskrivelse: str

# Create a new Facility
@router.post("/create/", response_model=FacilityResponse)  # Use the response schema here
async def create_facility(facility_data: FacilityCreate):
    facility = await Facility.create(**facility_data.dict())
    return facility

# Get all Facilities
@router.get("/", response_model=list[FacilityResponse])  # Use the response schema here
async def get_all_facilities():
    facilities = await Facility.all()
    return facilities
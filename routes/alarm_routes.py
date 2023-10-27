from fastapi import APIRouter, HTTPException
from models.alarm import SensorAlarm
from schemas.alarm_response import AlarmResponse  # Import the response schema
from pydantic import BaseModel  # Import BaseModel from Pydantic

router = APIRouter()

class AlarmCreate(BaseModel): # Class here as a DTO 
    type : str
    soner_id : int = None


# Create a new Facility
@router.post("/create/", response_model=AlarmResponse)  # Use the response schema here
async def create_alarm(alarm_data: AlarmCreate):
    alarm = await SensorAlarm.create(**alarm_data.dict())
    return alarm

# Get all Facilities
@router.get("/", response_model=list[AlarmResponse])  # Use the response schema here
async def get_all_alarm():
    alarm = await SensorAlarm.all()
    return alarm
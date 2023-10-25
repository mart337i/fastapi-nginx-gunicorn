from fastapi import APIRouter, HTTPException
from models.pollution_sensor import PollutionSensor
from schemas.pollution_sensor_response import PollutionSensorResponse
 
router = APIRouter()

from pydantic import BaseModel

class PollutionSensorCreate(BaseModel):
    name: str
    value: float
    datetime: str
    building_id: int

class PollutionSensorUpdate(BaseModel):
    name: str = None
    value: float = None
    datetime: str = None
    building_id: int = None
 
# Create a new PollutionSensor
@router.post("/", response_model=PollutionSensorResponse)
async def create_pollution_sensor(sensor_data: PollutionSensorCreate):
    sensor = await PollutionSensor.create(**sensor_data.dict())
    return sensor

# Get all PollutionSensors
@router.get("/", response_model=list[PollutionSensorResponse])
async def get_all_pollution_sensors():
    sensors = await PollutionSensor.all()
    return sensors

# Get a PollutionSensor by ID
@router.get("/{sensor_id}", response_model=PollutionSensorResponse)
async def get_pollution_sensor(sensor_id: int):
    sensor = await PollutionSensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="PollutionSensor not found")
    return sensor

# Update a PollutionSensor by ID
@router.put("/{sensor_id}", response_model=PollutionSensorResponse)
async def update_pollution_sensor(sensor_id: int, sensor_data: PollutionSensorUpdate):
    sensor = await PollutionSensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="PollutionSensor not found")
    
    for field, value in sensor_data.dict(exclude_unset=True).items():
        setattr(sensor, field, value)
    
    await sensor.save()
    return sensor

# Delete a PollutionSensor by ID
@router.delete("/{sensor_id}", response_model=dict)
async def delete_pollution_sensor(sensor_id: int):
    sensor = await PollutionSensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="PollutionSensor not found")
    
    await sensor.delete()
    return {"message": "PollutionSensor deleted"}
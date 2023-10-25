from fastapi import APIRouter, HTTPException
from models.temperature_humidity_sensor import TemperatureHumiditySensor
from schemas.temp_humidity_sensor_response import TempHumiditySensorResponse
from pydantic import BaseModel  # Import BaseModel from Pydantic


router = APIRouter()

class TempHumiditySensorCreate(BaseModel):
    value: float
    name: str
    datetime: str
    building_id: int

class TempHumiditySensorUpdate(BaseModel):
    value: float = None
    name: str = None
    datetime: str = None
    building_id: int = None

# Create a new TemperatureHumiditySensor
@router.post("/", response_model=TempHumiditySensorResponse)
async def create_temp_humidity_sensor(sensor_data: TempHumiditySensorCreate):
    sensor = await TemperatureHumiditySensor.create(**sensor_data.dict())
    return sensor

# Get all TemperatureHumiditySensors
@router.get("/", response_model=list[TempHumiditySensorResponse])
async def get_all_temp_humidity_sensors():
    sensors = await TemperatureHumiditySensor.all()
    return sensors

# Get a TemperatureHumiditySensor by ID
@router.get("/{sensor_id}", response_model=TempHumiditySensorResponse)
async def get_temp_humidity_sensor(sensor_id: int):
    sensor = await TemperatureHumiditySensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="TemperatureHumiditySensor not found")
    return sensor

# Update a TemperatureHumiditySensor by ID
@router.put("/{sensor_id}", response_model=TempHumiditySensorResponse)
async def update_temp_humidity_sensor(sensor_id: int, sensor_data: TempHumiditySensorUpdate):
    sensor = await TemperatureHumiditySensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="TemperatureHumiditySensor not found")
    
    for field, value in sensor_data.dict(exclude_unset=True).items():
        setattr(sensor, field, value)
    
    await sensor.save()
    return sensor

# Delete a TemperatureHumiditySensor by ID
@router.delete("/{sensor_id}", response_model=dict)
async def delete_temp_humidity_sensor(sensor_id: int):
    sensor = await TemperatureHumiditySensor.get_or_none(id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="TemperatureHumiditySensor not found")
    
    await sensor.delete()
    return {"message": "TemperatureHumiditySensor deleted"}
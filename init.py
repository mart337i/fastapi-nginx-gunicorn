from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import Facility, Building, Sensor, Sensor_value,Alarm, SensorType, AlarmType
from config import engine
from datetime import datetime

router = APIRouter()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

@router.post("/set_up/")
def init_setup(facility : Facility, building : Building,session: Session = Depends(get_session)):

    # Creating sample Facility and related Buildings, Sensors, Sensor Values, and Alarms
    default_facility = facility or Facility(beskrivelse="Main Facility")
    session.add(default_facility)
    session.commit()

    default_building = building or Building(name="Building A", facility_id=default_building.id)
    session.add(default_building)
    session.commit()

    return {"message": "setup data created successfully"}
    

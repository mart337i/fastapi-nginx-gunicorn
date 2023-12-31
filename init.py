from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import Facility, Building, Sensor, Sensor_value,Alarm, SensorType, AlarmType, ThresholdSettings, WorkingHours
from config import engine
from datetime import datetime, time

router = APIRouter()

# Dependency to get the database session
def get_session():
    """
        Get the db session / db curser
    """
    with Session(engine) as session:
        yield session

@router.post("/set_up/")
def init_setup(facility: Facility, building: Building, session: Session = Depends(get_session)):
    """
        Used to setup a facility, a building and default config values
    """

    # Creating sample Facility and related Buildings, Sensors, Sensor Values, and Alarms
    default_facility = facility or Facility(beskrivelse="Main Facility")
    session.add(default_facility)
    session.commit()

    default_building = building or Building(name="Building A", facility_id=default_facility.id)
    session.add(default_building)
    session.commit()

    working_hours = WorkingHours(
        morning = time(8,00),
        evening = time(16,00),
    )

    session.add(working_hours)
    session.commit()
    session.refresh(working_hours)

    default_temp_thresholds = ThresholdSettings(
        sensor_type=SensorType.temperature,
        max_value=30,  
        low_value=0  
    )
    session.add(default_temp_thresholds)

    default_humid_thresholds = ThresholdSettings(
        sensor_type=SensorType.humidity,
        max_value=80, 
        low_value=30   
    )
    session.add(default_humid_thresholds)

    session.commit()

    return {"message": "Setup data created successfully"}
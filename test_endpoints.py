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

@router.get("/get_all/")
def get_all(session: Session = Depends(get_session)):
    data = {
        "facilities": session.query(Facility).all(),
        "buildings": session.query(Building).all(),
        "sensors": session.query(Sensor).all(),
        "sensors_vals": session.query(Sensor_value).all(),
        "alarms": session.query(Alarm).all()
    }
    return data
    

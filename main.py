from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, select
from models import Facility, Building, PollutionSensor, TempHumiditySensor, Alarm
from sample import router as sample_route
from config import engine
from sqlmodel import SQLModel

app = FastAPI()
SQLModel.metadata.create_all(engine)

app.include_router(sample_route, prefix="/sample", tags=["sample data"]) 

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/facility/", response_model=Facility)
def create_facility(facility: Facility, session: Session = Depends(get_session)):
    session.add(facility)
    session.commit()
    session.refresh(facility)
    return facility

@app.post("/building/", response_model=Building)
def create_building(building: Building, session: Session = Depends(get_session)):
    session.add(building)
    session.commit()
    session.refresh(building)
    return building

@app.post("/pollution_sensor/", response_model=PollutionSensor)
def create_pollution_sensor(sensor: PollutionSensor, session: Session = Depends(get_session)):
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

@app.post("/temp_humidity_sensor/", response_model=TempHumiditySensor)
def create_temp_humidity_sensor(sensor: TempHumiditySensor, session: Session = Depends(get_session)):
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

@app.post("/alarm/", response_model=Alarm)
def create_alarm(alarm: Alarm, session: Session = Depends(get_session)):
    session.add(alarm)
    session.commit()
    session.refresh(alarm)
    return alarm
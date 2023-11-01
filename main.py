from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, select,SQLModel
from models import Facility, Building, Sensor, Sensor_value,Alarm 
from config import engine
#from sample import router as sample_route
from datetime import datetime,timedelta

from init import router as startup_route

app = FastAPI()
SQLModel.metadata.create_all(engine)

#app.include_router(sample_route, prefix="/sample", tags=["sample data"]) 
app.include_router(startup_route, prefix="/setup", tags=["setup service"]) 

#Defaults for sensor setup.
TARGET_BUILDING = 1
TARGET_FACILITY = 1
TARGET_NAME = "DT22"

def get_session():
    """
        get the database session located in the file config.
        i created the connection in a diffrent file to make sure it could be used by multible models.
        this also avoids import errors
    """
    with Session(engine) as session:
        yield session

@app.post("/change_taget_building/")
def Change_taget_buidling(builing_id : int):
    TARGET_BUILDING = Building
@app.post("/change_taget_facility/")
def change_taget_facility(facility_id : int):
    TARGET_FACILITY = Facility

@app.post("/change_taget_name/")
def change_taget_facility(sensor_name : str):
    TARGET_NAME = sensor_name

@app.get("/get_taget_building/")
def get_taget_buidling():
    return TARGET_BUILDING

@app.get("/get_taget_facility/")
def get_taget_facility():
    return TARGET_FACILITY

@app.get("/get_taget_name/")
def get_taget_name():
    return TARGET_NAME


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

@app.post("/create_sensor/", response_model=Sensor)
def create_sensor(sensor: Sensor, session: Session = Depends(get_session)):
    sensor = Sensor(name=sensor.name, building_id=sensor.building_id)
    session.add(sensor)
    session.commit()
    return sensor

@app.post("/sensor_value/", response_model=Sensor_value)
def sensor_value(sensor_value: Sensor_value, session: Session = Depends(get_session)):
    session.add(sensor_value)
    session.commit()
    session.refresh(sensor_value)
    return sensor_value

@app.post("/alarm/", response_model=Alarm)
def create_alarm(alarm: Alarm, session: Session = Depends(get_session)):
    session.add(alarm)
    session.commit()
    session.refresh(alarm)
    return alarm

@app.get("/get-sample-data/")
def get_sample_data(session: Session = Depends(get_session)):
    data = {
        "facilities": session.query(Facility).all(),
        "buildings": session.query(Building).all(),
        "sensor": session.query(Sensor).all(),
        "sensor_value": session.query(Sensor_value).all(),
        "alarms": session.query(Alarm).all()
    }

    return data

@app.get("/dashboard/")
def get_dashboard(session: Session = Depends(get_session)):
    # Get the last 10 sensor values based on datetime
    sensors_vals = session.query(Sensor_value).order_by(Sensor_value.value_datetime.desc()).limit(10).all()

    if not sensors_vals:
        raise HTTPException(status_code=204, detail="No sensor records found")
    
    # Fetch all alarms
    alarms = session.query(Alarm).all()

    return {"sensors": sensors_vals, "alarms": alarms}
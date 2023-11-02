from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine, select,SQLModel
from models import Facility, Building, Sensor, Sensor_value,Alarm ,SensorType ,AlarmType
from config import engine
from typing import List
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


#----------------Create new sensor----------------------------#
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

#----------------------------------------------------------------#


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
    # Check if a sensor with the same serial_number already exists
    try:
        existing_sensor = session.execute(select(Sensor).where(Sensor.serial_number == sensor.serial_number)).first()
        return existing_sensor
    except SQLAlchemyError as e:
    # Handle the exception here
        print(f"An error occurred: {e}")
        existing_sensor = None  # Set existing_sensor to None or another suitable value in case of an error

    # Create a new sensor
    new_sensor = Sensor(name=sensor.name, building_id=sensor.building_id, serial_number=sensor.serial_number)
    session.add(new_sensor)
    session.commit()
    return new_sensor

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

@app.get("/get_sensor_by_serial/{serial_number}", response_model=Sensor)
def get_sensor_by_serial(serial_number: str, db: Session = Depends(get_session)):
    sensor = db.exec(select(Sensor).where(Sensor.serial_number == serial_number)).one_or_none()
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with serial number {serial_number} not found")
    return sensor

@app.get("/dashboard/")
def get_dashboard(session: Session = Depends(get_session)):
    sensors_vals = session.query(Sensor_value).order_by(Sensor_value.value_datetime.desc()).limit(10).all()

    if not sensors_vals:
        raise HTTPException(status_code=204, detail="No sensor records found")
    
    # Fetch all alarms
    alarms = session.query(Alarm).all()

    return {"sensors": sensors_vals, "alarms": alarms}


@app.get("/get_sensor_data/{sensor_id}", response_model=dict)
def get_temp_data(sensor_id: int, session: Session = Depends(get_session)):
    # Check if the sensor exists
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    latest_sensor_data = (
        session.query(Sensor_value)
        .filter(
            Sensor_value.sensor_id == sensor_id,
            Sensor_value.sensorType == SensorType.temperature  # Replace with the actual value
        )
        .order_by(Sensor_value.value_datetime.desc())
        .limit(1)
        .one_or_none()
    )

    if not latest_sensor_data:
        raise HTTPException(status_code=404, detail="Sensor data not found")

    # Check if the sensor data is outside the specified range for the sensor type
    sensor_type = latest_sensor_data.sensorType
    low_value = latest_sensor_data.low_value_temp
    max_value = latest_sensor_data.max_value_temp

    value = latest_sensor_data.value

    alarm_triggered = (
        (low_value is not None and value < low_value) or (max_value is not None and value > max_value)
    )

    if alarm_triggered:
        alarm_type = AlarmType.warning
        alarm_msg = f"Sensor {sensor.serial_number} returned {latest_sensor_data.value}:typeof({latest_sensor_data.sensorType} at {latest_sensor_data.value_datetime})"
        alarm = Alarm(type=alarm_type, msg=alarm_msg, sonor_id=sensor.id)
        session.add(alarm)
        session.commit()

    return {
        "sensor_id": sensor.id,
        "name": sensor.name,
        "sensor_type": sensor_type,
        "value": value,
        "value_datetime": latest_sensor_data.value_datetime,
        "alarm_triggered": alarm_triggered
    }

@app.get("/get_all_sensor_serial_numbers", response_model=List[Sensor])
def get_all_sensor_serial_numbers(session: Session = Depends(get_session)):
    # Query all sensor serial numbers
    serial_numbers = session.exec(select(Sensor.serial_number)).all()

    # Retrieve sensor objects based on the serial numbers
    sensors = (
        session.exec(select(Sensor).where(Sensor.serial_number.in_(serial_numbers)))
        .all()
    )

    return sensors
from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import Facility, Building, Sensor, Sensor_value,Alarm , AlarmType, SensorType
from config import engine

router = APIRouter()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session


@router.post("/insert-sample-data/")
def insert_sample_data(session: Session = Depends(get_session)):
    # Sample data for Facility
    facility1 = Facility(beskrivelse="Facility 1 Description")
    facility2 = Facility(beskrivelse="Facility 2 Description")

    session.add(facility1)
    session.add(facility2)
    session.commit()

    # Sample data for Building
    building1 = Building(name="Building 1", facility_id=facility1.id)
    building2 = Building(name="Building 2", facility_id=facility2.id)

    session.add(building1)
    session.add(building2)
    session.commit()

    # Sample data for PollutionSensor
    sensor1 = PollutionSensor(name="Sensor 1", value=20.5, datetime="2023-10-28T10:30:00", building_id=building1.id)
    sensor2 = PollutionSensor(name="Sensor 2", value=22.3, datetime="2023-10-28T11:30:00", building_id=building2.id)

    session.add(sensor1)
    session.add(sensor2)
    session.commit()

    # Sample data for TempHumiditySensor
    temp_sensor1 = TempHumiditySensor(type=SensorType.temperature, value=23.0, name="Temp Sensor 1", datetime="2023-10-28T12:00:00", building_id=building1.id)
    humidity_sensor1 = TempHumiditySensor(type=SensorType.humidity, value=55.0, name="Humidity Sensor 1", datetime="2023-10-28T12:05:00", building_id=building2.id)

    session.add(temp_sensor1)
    session.add(humidity_sensor1)
    session.commit()

    # Sample data for Alarm
    alarm1 = Alarm(type=AlarmType.warning, sonor_id=1)
    alarm2 = Alarm(type=AlarmType.good, sonor_id=2)
    alarm3 = Alarm(type=AlarmType.failure,message="IO ERROR", sonor_id=2)

    session.add(alarm1)
    session.add(alarm2)
    session.add(alarm3)
    session.commit()

    return {"message": "Sample data inserted successfully!"}


@router.get("/get-sample-data/")
def get_sample_data(session: Session = Depends(get_session)):
    data = {
        "facilities": session.query(Facility).all(),
        "buildings": session.query(Building).all(),
        "pollution_sensors": session.query(PollutionSensor).all(),
        "temp_humidity_sensors": session.query(TempHumiditySensor).all(),
        "alarms": session.query(Alarm).all()
    }
    return data
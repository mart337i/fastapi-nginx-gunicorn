from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine, select,SQLModel
from models import Facility, Building, Sensor, Sensor_value,Alarm ,SensorType ,AlarmType,ThresholdSettings
from config import engine
from typing import List
from datetime import datetime,timedelta
import logging

from init import router as startup_route
from test_endpoints import router as test_route


logging.basicConfig(filename='/home/sysadmin/code/fastapi-nginx-gunicorn/logs/application.log',  # log to a file named 'app.log'
                    filemode='a',  # append to the log file if it exists, otherwise create it
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

_logger = logging.getLogger(__name__)


app = FastAPI()
SQLModel.metadata.create_all(engine)

app.include_router(startup_route, prefix="/setup", tags=["setup service"]) 
app.include_router(test_route, prefix="/test", tags=["test service"]) 

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

#---------------Root------------------------------------------#

@app.get("/", response_class=HTMLResponse)
def root():
    return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Greenhouse API</title>
                <!-- Include Bootstrap CSS from CDN -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body class="bg-light">
                <div class="container py-5">
                    <h1 class="display-4 text-center mb-3">Welcome to the Greenhouse Temperature and Humidity API</h1>
                    <p class="lead text-center mb-5">Use the links below to navigate to the API documentation:</p>
                    <div class="row">
                        <div class="col-md-6 text-center mb-3">
                            <a href="/docs" class="btn btn-primary btn-lg">Swagger UI Documentation</a>
                        </div>
                        <div class="col-md-6 text-center mb-3">
                            <a href="/redoc" class="btn btn-secondary btn-lg">ReDoc Documentation</a>
                        </div>
                    </div>
                </div>
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            </body>
            </html>

    """

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
    db_sensor = session.exec(select(Sensor).where(Sensor.serial_number == sensor.serial_number)).first()
    if db_sensor is not None:
        # The sensor already exists, return it
        return db_sensor

    # Create a new sensor since it doesn't exist
    new_sensor = Sensor(serial_number=sensor.serial_number, name=sensor.name, building_id=sensor.building_id)
    session.add(new_sensor)
    session.commit()  # After committing, new_sensor should have the new ID populated
    session.refresh(new_sensor)

    return new_sensor  # Return the new sensor with the ID

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
    # Join Sensor and Sensor_value to get both models
    sensors_vals = (
        session.exec(
            select(Sensor, Sensor_value)
            .join(Sensor_value)
            .order_by(Sensor_value.value_datetime.desc())
            .limit(10)
        )
        .all()
    )

    if not sensors_vals:
        raise HTTPException(status_code=204, detail="No sensor records found")
    
    alarms = session.query(Alarm).all()
    alarms = [alarm for alarm in alarms]
    
    _logger.warning(f"sensors : {sensors_vals}")

    return {"sensor_values": sensors_vals, "alarms": alarms}


@app.get("/get_temp_data/{sensor_id}", response_model=dict)
def get_temp_data(sensor_id: int, session: Session = Depends(get_session)):
    # Check if the sensor exists
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # Fetch the global threshold settings for temperature sensors
    temp_thresholds = session.query(ThresholdSettings).filter_by(sensor_type=SensorType.temperature).first()
    if not temp_thresholds:
        raise HTTPException(status_code=404, detail="Temperature threshold settings not found")

    # Get the latest temperature data for the sensor
    latest_sensor_data = (
        session.query(Sensor_value)
        .filter(Sensor_value.sensor_id == sensor_id, Sensor_value.sensorType == SensorType.temperature)
        .order_by(Sensor_value.value_datetime.desc())
        .limit(1)
        .one_or_none()
    )

    if not latest_sensor_data:
        raise HTTPException(status_code=404, detail="Temperature data not found for sensor")

    # Check if the latest sensor data is outside the global threshold range
    value = latest_sensor_data.value
    alarm_triggered = (
        (temp_thresholds.low_value is not None and value < temp_thresholds.low_value) or
        (temp_thresholds.max_value is not None and value > temp_thresholds.max_value)
    )

    # If the value is out of range, create an alarm
    if alarm_triggered:
        alarm_msg = f"Sensor {sensor.serial_number} reported temperature {value} at {latest_sensor_data.value_datetime}, which is outside of the set thresholds."
        alarm = Alarm(type=AlarmType.warning, msg=alarm_msg, serial_number=sensor.serial_number)
        session.add(alarm)
        session.commit()

    return {
        "sensor_id": sensor.id,
        "name": sensor.name,
        "sensor_type": SensorType.temperature.value,
        "value": value,
        "value_datetime": latest_sensor_data.value_datetime.isoformat(),
        "alarm_triggered": alarm_triggered
    }

@app.get("/get_humid_data/{sensor_id}", response_model=dict)
def get_humid_data(sensor_id: int, session: Session = Depends(get_session)):
    # Check if the sensor exists
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # Fetch the global threshold settings for temperature sensors
    humid_thresholds = session.query(ThresholdSettings).filter_by(sensor_type=SensorType.humidity).first()
    if not humid_thresholds:
        raise HTTPException(status_code=404, detail="Temperature threshold settings not found")

    # Get the latest temperature data for the sensor
    latest_sensor_data = (
        session.query(Sensor_value)
        .filter(Sensor_value.sensor_id == sensor_id, Sensor_value.sensorType == SensorType.humidity)
        .order_by(Sensor_value.value_datetime.desc())
        .limit(1)
        .one_or_none()
    )

    if not latest_sensor_data:
        raise HTTPException(status_code=404, detail="Temperature data not found for sensor")

    # Check if the latest sensor data is outside the global threshold range
    value = latest_sensor_data.value
    alarm_triggered = (
        (humid_thresholds.low_value is not None and value < humid_thresholds.low_value) or
        (humid_thresholds.max_value is not None and value > humid_thresholds.max_value)
    )

    # If the value is out of range, create an alarm
    if alarm_triggered:
        alarm_msg = f"Sensor {sensor.serial_number} reported temperature {value} at {latest_sensor_data.value_datetime}, which is outside of the set thresholds."
        alarm = Alarm(type=AlarmType.warning, msg=alarm_msg, serial_number=sensor.serial_number)
        session.add(alarm)
        session.commit()

    return {
        "sensor_id": sensor.id,
        "name": sensor.name,
        "sensor_type": SensorType.temperature.value,
        "value": value,
        "value_datetime": latest_sensor_data.value_datetime.isoformat(),
        "alarm_triggered": alarm_triggered
    }


@app.put("/threshold-settings/", response_model=ThresholdSettings)
def update_threshold_settings(
    sensor_type: SensorType, max_value: int, low_value: int, session: Session = Depends(get_session)
):
    # Select the first ThresholdSettings record that matches the sensor_type
    existing_settings = session.exec(
        select(ThresholdSettings).where(ThresholdSettings.sensor_type == sensor_type)
    ).first()

    _logger.warning(f"existing_settings : {existing_settings}")

    if not existing_settings:
        # If no record is found, return a message instead of raising an exception
        return {"message": "ThresholdSettings not found for the specified sensor type"}

    # Update the existing ThresholdSettings with the new values
    existing_settings.max_value = max_value
    existing_settings.low_value = low_value
    
    session.add(existing_settings)
    session.commit()
    session.refresh(existing_settings)
    
    return existing_settings

@app.get("/threshold-settings/", response_model=list)
def get_threshold_settings(session: Session = Depends(get_session)):
    # Select the first ThresholdSettings record
    settings = session.exec(select(ThresholdSettings)).all()
    _logger.warning(f"settings : {settings}")
    if not settings:
        raise HTTPException(status_code=404, detail="ThresholdSettings not found")
    
    return settings

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
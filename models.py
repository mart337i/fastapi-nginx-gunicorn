from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, time
    
class SensorType(str, Enum):
    """
        Type Enum
        @params : {
        str : enum 
        }
    """
    temperature = "temperature"
    humidity = "humidity"

class AlarmType(str, Enum):
    """
        Type Enum

        @params : {
        str : enum 
        }
    """
    warning = "warning"
    failure = "failure"
    good = "good"

class WorkingHours(SQLModel, table=True):
    """
        Woking Hours model 
        @Params {
            # Id is auto set,
            morning : time() object 
            evening : time() object
            # created_date is autoset  
        }
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    morning : Optional[time]
    evening : Optional[time]
    created_date : Optional[datetime] = datetime.utcnow().isoformat()

class ThresholdSettings(SQLModel, table=True):
    """
        ThresholdSettings model
        Lets you set max and min values for SensorType
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_type: SensorType  
    max_value: int
    low_value: int

class Facility(SQLModel, table=True):
    """
        Facility model 
        contains a collection of buildings

        #TODO if i had time this would also contain addresss, employees, etc 

    """
    id: Optional[int] = Field(primary_key=True, index=True)
    beskrivelse: str = Field()
    buildings: list["Building"] = Relationship(back_populates="facility")

    
class Building(SQLModel, table=True):
    """
        Building model
        NOTE A building is interpreted as a greenhouse but i should have abstraed it a layer more with rooms for pressions

        A building contaions a list of sensors and a ref to the faciliy it located in 
    """
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    facility_id: int = Field(foreign_key="facility.id")
    facility: Facility = Relationship(back_populates="buildings")
    sensor: list["Sensor"] = Relationship()

class Sensor(SQLModel, table=True):
    """
        Sensor model
        A sensor in this case has a sensor values, the sensor in this case is apstrated to the indevidual program running on the client
        It is part of a building, and i can have any name using the @param name : str. 
        The @param serial_number has to be uniqe for each device 
    """
    id: Optional[int] = Field(primary_key=True, index=True)
    serial_number: Optional[str] = Field(unique=True, index=True)
    name: str
    building_id: int = Field(foreign_key="building.id")
    sensor_value: list["Sensor_value"] = Relationship()
    alarm: list["Alarm"] = Relationship()
    sensor: Building = Relationship(back_populates="sensor")

class Sensor_value(SQLModel, table=True):
    """
        Sensor_value model
        For this it only contains the nessesary types for temp and humid,
        but chould easily be expaned by defining chnaging the @param value's name to value_<datatype> 
        and having one foreach datatype and then expanding on the sensor type enum, but then every value would have to be Optional
    """
    id: Optional[int] = Field(primary_key=True, index=True)
    sensorType: SensorType
    value: float
    value_datetime: Optional[datetime] = datetime.utcnow().isoformat()
    sensor_id: int = Field(foreign_key="sensor.id")
    sensor_value: Sensor = Relationship(back_populates="sensor_value")


class Alarm(SQLModel, table=True):
    """
        Alarm model
        Keeps record of alarms created by the server itself or the client
    """
    id: Optional[int] = Field(primary_key=True, index=True)
    type: AlarmType
    msg : str = None
    serial_number: str = Field(foreign_key="sensor.serial_number")
    sensor: Sensor = Relationship(back_populates="alarm")


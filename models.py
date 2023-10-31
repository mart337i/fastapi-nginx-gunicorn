from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
    
class SensorType(str, Enum):
    temperature = "temperature"
    humidity = "humidity"

class AlarmType(str, Enum):
    warning = "warning"
    failure = "failure"
    good = "good"

class Facility(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    beskrivelse: str = Field()
    buildings: list["Building"] = Relationship(back_populates="facility")

    
class Building(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    facility_id: int = Field(foreign_key="facility.id")
    facility: Facility = Relationship(back_populates="buildings")
    sensor: list["Sensor"] = Relationship()

class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    building_id: int = Field(foreign_key="building.id")
    sensor_value: list["Sensor_value"] = Relationship()
    alarm: list["Alarm"] = Relationship()
    sensor: Building = Relationship(back_populates="sensor")

class Sensor_value(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    type: SensorType
    max_value : int 
    low_value : int
    value: float
    datetime: str
    sensor_id: int = Field(foreign_key="sensor.id")
    sensor_value: Sensor = Relationship(back_populates="sensor_value")


class Alarm(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    type: AlarmType
    msg : str = None
    sonor_id: int = Field(foreign_key="sensor.id")
    sensor: Sensor = Relationship(back_populates="alarm")


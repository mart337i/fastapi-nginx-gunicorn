from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

class SensorType(str, Enum):
    temperature = "temperature"
    humidity = "humidity"

class AlarmType(str, Enum):
    warning = "warning"
    failure = "failure"
    good = "good"

class Facility(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    beskrivelse: str = Field()
    buildings: list["Building"] = Relationship(back_populates="facility")

class Building(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    facility_id: int = Field(foreign_key="facility.id")
    facility: Facility = Relationship(back_populates="buildings")
    pollution_sensors: list["PollutionSensor"] = Relationship()
    temp_humidity_sensors: list["TempHumiditySensor"] = Relationship()

class PollutionSensor(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    value: float
    datetime: str
    building_id: int = Field(foreign_key="building.id")

class TempHumiditySensor(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    type: SensorType
    value: float
    name: str
    datetime: str
    building_id: int = Field(foreign_key="building.id")

class Alarm(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    type: AlarmType
    sonor_id: int

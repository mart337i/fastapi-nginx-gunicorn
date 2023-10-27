from tortoise import fields
from tortoise.models import Model
from enum import Enum

class AlarmType(str, Enum):
    warning = "warning"
    failure = "failure"
    good = "good"
    low = "low"


class SensorAlarm(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=20, choices=[(e.value, e.value) for e in AlarmType])
    sonor_id = fields.IntField()

    class Meta:
        table = "Alarm"

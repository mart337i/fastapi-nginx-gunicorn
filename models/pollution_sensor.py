from tortoise import fields
from tortoise.models import Model

class PollutionSensor(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    datetime = fields.DatetimeField()
    building = fields.ForeignKeyField("models.Building", related_name="pollution_sensors")

    class Meta:
        table = "PollutionSensor"

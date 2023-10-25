from tortoise import fields
from tortoise.models import Model

class TemperatureHumiditySensor(Model):
    id = fields.IntField(pk=True)
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    name = fields.CharField(max_length=255)
    datetime = fields.DatetimeField()
    building = fields.ForeignKeyField("models.Building", related_name="temp_humidity_sensors")

    class Meta:
        table = "TemperatureHumiditySensor"

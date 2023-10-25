from tortoise import fields
from tortoise.models import Model

class Building(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    facility = fields.ForeignKeyField("models.Facility", related_name="buildings")

    class Meta:
        table = "Building"

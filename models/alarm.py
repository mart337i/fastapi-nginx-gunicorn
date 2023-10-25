from tortoise import fields
from tortoise.models import Model

class Alarm(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=30)
    beskrivelse = fields.CharField(max_length=255,null=True)

    class Meta:
        table = "Alarm"

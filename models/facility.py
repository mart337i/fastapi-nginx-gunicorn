from tortoise import fields
from tortoise.models import Model

class Facility(Model):
    id = fields.IntField(pk=True)
    beskrivelse = fields.CharField(max_length=255)

    class Meta:
        table = "Facility"

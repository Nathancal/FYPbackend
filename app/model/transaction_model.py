from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateTimeField, IntField, StringField, FloatField


class Transactions(EmbeddedDocument):
    
    milestransId = StringField(required=True, unique=True)
    pickupId = StringField()
    totalNumPassengers = IntField()
    totalMilesTravelled = FloatField()

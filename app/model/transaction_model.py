from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateTimeField, IntField, StringField, FloatField, BooleanField


class Transactions(EmbeddedDocument):
    
    milestransId = StringField()
    pickupId = StringField()
    totalNumPassengers = IntField()
    totalMilesTravelled = FloatField()
    isHost = BooleanField()
    embarkAddress = StringField()
    returnAddress = StringField()
    completedAt = DateTimeField()

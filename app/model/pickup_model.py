from mongoengine.fields import PointField, DynamicField, DateTimeField, ListField, StringField, IntField, FloatField
from mongoengine.document import Document

class Pickup(Document):

    pickupId = StringField(required=True)  
    embarkLocation = PointField()
    returnLocation = PointField()
    hostId = DynamicField()
    address = StringField()
    date = DynamicField()
    embarkAddress = DynamicField()
    returnAddress = DynamicField()
    time = DynamicField()
    createdAt = DateTimeField()
    totalNumPassengers = IntField()
    passengers = ListField()
    pickupStatus = StringField()
    journeyStartedAt = DateTimeField()
    journeyCompletedAt = DateTimeField()
    duration = FloatField()
    milesTravelled = DynamicField()

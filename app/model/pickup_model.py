from mongoengine.fields import PointField, DynamicField, DateTimeField, ListField, StringField, IntField
from mongoengine.document import Document

class Pickup(Document):

    pickupId = StringField(required=True)  
    location = PointField()
    hostId = DynamicField()
    address = StringField()
    date = DynamicField()
    time = DynamicField()
    createdAt = DateTimeField()
    totalNumPassengers = IntField()
    passengers = ListField()
    pickupStatus = StringField()
    startedAt = DateTimeField()
    completedAt = DateTimeField()
    milesTravelled = DynamicField()
from mongoengine.fields import PointField, DynamicField, DateTimeField, ListField, StringField
from mongoengine.document import Document

class Pickup(Document):

    pickupId = StringField(required=True)  
    location = PointField()
    hostId = DynamicField()
    address = StringField()
    date = DynamicField()
    time = DynamicField()
    createdAt = DateTimeField()
    passengers = ListField()

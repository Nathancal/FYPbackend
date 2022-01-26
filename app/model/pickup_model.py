from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document

class Pickup(Document):

    pickupId = StringField(required=True)
    lat = DynamicField()
    lng = DynamicField()
    hostId = DynamicField()
    address = StringField()
    date = DynamicField()
    time = DynamicField()
    passengers = ListField()

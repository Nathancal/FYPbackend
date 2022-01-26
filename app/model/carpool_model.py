from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document

class Carpool(Document):
    carpoolId = StringField(required=True)
    firstPickupId = DynamicField()
    secondPickupId = DynamicField()
    hostId = DynamicField()
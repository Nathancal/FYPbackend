from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, DecimalField, EmailField, EmbeddedDocumentField, ListField, StringField
impor

class Pickup(Document):

    pickupId = StringField(required=True)
    lat = DecimalField(required=True)
    lng = DecimalField(required=True)
    hostId = StringField(required=True)
    address = StringField(required=True)
    passengers = ListField(EmbeddedDocumentField())
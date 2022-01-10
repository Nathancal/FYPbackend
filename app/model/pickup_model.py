from mongoengine.fields import BooleanField, DateTimeField, DecimalField, EmailField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document, EmbeddedDocument
from app.model.user_model import User

class Pickup(Document):

    pickupId = StringField(required=True)
    lat = DecimalField(required=True)
    lng = DecimalField(required=True)
    hostId = StringField(required=True)
    address = StringField(required=True)
    date = DateTimeField()
    passengers = ListField(EmbeddedDocumentField(User))
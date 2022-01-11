from flask.scaffold import F
from mongoengine.fields import BooleanField, DateTimeField, DecimalField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document
from app.model.user_model import UserEmb

class Pickup(Document):

    pickupId = StringField(required=True)
    lat = DecimalField(required=True)
    lng = DecimalField(required=True)
    hostId = StringField(required=True)
    address = StringField(required=True)
    date = DateTimeField()
    completed = BooleanField(default=False)
    passengers = ListField(EmbeddedDocumentField(UserEmb))
from sqlite3 import Date
from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document

class Message(Document):

    messageId = StringField(required=True)
    senderId = StringField()
    recepientId = StringField()
    associatedPickupId = StringField()
    text = StringField()
    sentAt = DateTimeField()
    received = BooleanField(default=False)
    receivedAt = DateTimeField()

from sqlite3 import Date
from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import EmbeddedDocument

class Message(EmbeddedDocument):

    messageId = StringField()
    userSentId = StringField()
    text = StringField()
    sentAt = DateTimeField()
    received = BooleanField(default=False)
    receivedAt = DateTimeField()

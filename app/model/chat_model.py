from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document

class Chat(Document):

    chatId = StringField(required=True)
    chatMemberOne = StringField()
    chatMemberTwo = StringField()
    associatedPickupId = StringField()
    createdAt = DateTimeField()
    closed = BooleanField()

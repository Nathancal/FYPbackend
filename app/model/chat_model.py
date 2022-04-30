from mongoengine.fields import BooleanField, DateTimeField, DecimalField, DynamicField, EmbeddedDocumentField, ListField, StringField
from mongoengine.document import Document

from app.model.message_model import Message

class Chat(Document):

    chatId = StringField()
    chatMemberOneId = StringField()
    chatMemberTwoId = StringField()
    messages = ListField(EmbeddedDocumentField(Message))
    createdAt = DateTimeField()
    closed = BooleanField(default=False)

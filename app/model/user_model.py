from mongoengine.fields import BooleanField, EmailField, StringField
from mongoengine.document import Document, EmbeddedDocument

class User(EmbeddedDocument):
        
        userID = StringField(required=True)
        email = EmailField(required=True, unique=True)
        firstName = StringField(max_length=40, required=True)
        lastName = StringField(max_length=40, required=True)
        password = StringField(required=True)
        admin = BooleanField(default=False)

class UserDoc(Document):

        userID = StringField(required=True)
        email = EmailField(required=True, unique=True)
        firstName = StringField(max_length=40, required=True)
        lastName = StringField(max_length=40, required=True)
        password = StringField(required=True)
        admin = BooleanField(default=False)
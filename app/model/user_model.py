from email.policy import default
from mongoengine.fields import BooleanField,DecimalField, EmailField, StringField, IntField, ListField, EmbeddedDocumentField
from mongoengine.document import Document

from app.model.user_rating_model import userRating

class User(Document):

        userID = StringField(required=True, unique=True)
        email = EmailField(required=True, unique=True)
        firstName = StringField(max_length=40, required=True)
        lastName = StringField(max_length=40, required=True)
        password = StringField(required=True)
        admin = BooleanField(default=False)
        newUser = BooleanField(default=True)
        totalJourneys = IntField(default=0)
        totalMiles = DecimalField(default=20.00)
        avgScore = DecimalField(default=3.75)
        reviews = ListField(EmbeddedDocumentField(userRating))


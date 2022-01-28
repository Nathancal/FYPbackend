from email.policy import default
from tokenize import String
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import BooleanField, IntField, DecimalField, StringField


class userRating(EmbeddedDocument):

    ratingId = StringField(required=True)
    hostId = StringField(required=True)
    userId = StringField(required=True)
    score = DecimalField(default=3.75)
    comment = StringField()
    newUser = BooleanField(default=True)



from email.policy import default
from tokenize import String
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import  DecimalField, StringField, DateTimeField


class userRating(EmbeddedDocument):

    ratingId = StringField(required=True)
    userPostedId = StringField(required=True)
    score = DecimalField(required=True)
    comment = StringField()
    date = DateTimeField()



from mongoengine.fields import BooleanField, EmailField, StringField


class User():
        
        userID = StringField(required=True)
        email = EmailField(required=True, unique=True)
        firstName = StringField(max_length=40, required=True)
        lastName = StringField(max_length=40, required=True)
        password = StringField(required=True)
        admin = BooleanField(default=False)

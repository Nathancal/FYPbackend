import uuid
import datetime
from flask import request
from app.model.message_model import Message

def create_message():


    try:
            
        message = Message()

        message.messageId = uuid.uuid4().hex
        message.senderId = request.json["userId"]
        message.recepientId = request.json["recepientId"]
        message.associatedPickupId = request.json["pickupId"]
        message.text = request.json["message"]
        message.sentAt = datetime.datetime.utcnow()

        message.save()
    except:
        
import uuid
import datetime
from flask import jsonify, make_response, request
from app.model.message_model import Message
from app.utility.parsejson_utility import parse_json

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


        return make_response(jsonify({
            "message": "message successfully sent.",
            "date": datetime.datetime.utcnow()
        }))

    except Exception as e:
        return make_response(jsonify({
            "message": "unable to create message, please try again."
        },e), 500)

def get_message():

    messageCol = Message._get_collection()

    message = messageCol.find({
        "messageId": request.json["messageId"]
    })

    if message is not None:

        return make_response(jsonify({
            "message": "message has been found.",
            "data": parse_json(message)

        }))

def get_all_

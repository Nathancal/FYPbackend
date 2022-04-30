import uuid
import datetime
from flask import jsonify, make_response, request
from app.model.chat_model import Chat
from app.model.message_model import Message

from app.utility.parsejson_utility import parse_json

def create_message():


    try:

        chat = Chat.objects.get(chatId=request.json["chatId"])

            
        message = Message()

        message.messageId = uuid.uuid4().hex
        message.text = request.json["message"]
        message.userSentId = request.json["userId"]
        message.sentAt = datetime.datetime.utcnow()

        chat.messages.append(message)
        chat.save()


        return make_response(jsonify({
            "message": "message successfully sent.",
            "date": datetime.datetime.utcnow()
        }))

    except Exception as e:
        return make_response(jsonify({
            "message": "unable to create message, please try again."
        },e), 500)


def read_messages():

    try:

        chat = Chat()._get_collection()

        chatFound = chat.find_one({
            "chatId": request.json["chatId"]
        })

        if chatFound is not None:

            if chatFound["messages"] is not None:


                for message in chatFound["messages"]:

                    if message["received"] is not None:

                        message["received"] = True

                chatUpdate = chat.update_one({"chatId": request.json["chatId"]}, {"$set" :{chatFound}})

                return make_response(jsonify({
                    "message": "messages successfully updated."
                }),201)

            else:

                return make_response(jsonify({
                    "message": "no messages have been found associated with this chat."
                }),404)
        else:

            return make_response(jsonify({
                "message": "this chat has not been found"
            }),404)
    except Exception as e:

        return make_response(jsonify({
            "message": "an unknown exception as occoured."
        }),404)
from xml.dom import NotFoundErr
from flask import jsonify, make_response, request
import uuid
import datetime
from flask import jsonify, make_response, request
from app.utility.parsejson_utility import parse_json


from app.model.chat_model import Chat


def create_chat():

    try:

        chat = Chat()

        chat.chatId = uuid.uuid4().hex
        chat.chatMemberOneId = request.json["userId"]
        chat.chatMemberTwoId = request.json["userSelectedId"]
        chat.createdAt = datetime.datetime.utcnow()

        chat.save()

        return make_response(jsonify({
            "message": "chat successfully created.",
            "data": chat.chatId
        }),200)
    except Exception as e:
        return make_response(jsonify({
            "message": "error occoured creating chat try again",
            "error": e
        }),401)

def get_all_chats_for_user():

    getChats = Chat()._get_collection()

    try:
        chatsFound = getChats.find(
            {"$or": [
                {"chatMemberOneId": request.json["userId"]},
                {"chatMemberTwoId": request.json["userId"]},
            ]}, {"_id": 0})

        return make_response(jsonify({
            "message": "chats have been found.",
            "data": parse_json(chatsFound)
        }))

    except NotFoundErr as e:
        return make_response(jsonify({
            "message": "no chats have been found for this user",
            "data": []
        }))


def check_chat_exist():

    getChats = Chat()._get_collection()

    try:

        print("has chat been found?")
        chatsFound = getChats.find(
            {"$or": [

                {
                    "$and": [{"chatMemberOneId": request.json["userId"]},
                             {"chatMemberTwoId": request.json["recepUserId"]},
                             ]
                }, {
                    "$and": [{"chatMemberOneId": request.json["recepUserId"]},
                             {"chatMemberTwoId": request.json["userId"]}, ]
                }

            ]}, {"_id": 0})
        print("si")
        return make_response(jsonify({
            "message": "chat has been found.",
            "data": parse_json(chatsFound)
        }))

    except NotFoundErr as e:
        print("claro que no ")
        return make_response(jsonify({
            "message": "no chat has been found between these users."
        }),404)

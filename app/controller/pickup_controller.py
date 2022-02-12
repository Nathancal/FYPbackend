from ast import parse
from datetime import datetime
import re
from xml.etree.ElementTree import PI
from mongoengine.errors import ValidationError
from app.model.pickup_model import Pickup
from app.model.user_model import User
import uuid
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify
from pymongo import GEO2D


def create_pickup_point():

    try:
        print(request.json["hostId"])

        lat = request.json["lat"]
        lng = request.json["lng"]

        locationObj = {
            'type': 'Point',
            'coordinates': [lat, lng]
        }

        pickup = Pickup()
        pickup.pickupId = uuid.uuid4().hex
        pickup.hostId = request.json["hostId"]
        pickup.location = locationObj
        pickup.createdAt = datetime.utcnow
        pickup.date = request.json["date"]
        pickup.time = request.json["time"]
        pickup.address = request.json["address"]

        pickup.save()

        return make_response(jsonify({
            "message": "rendezvous successfully created!",
            "address": parse_json(pickup.address)
        }))
    except ValidationError as e:
        error = e.message
        return make_response(jsonify({
            "message": "some fields may be empty please try again.",
            "error": error
        }), 404)

    except TypeError as e:
        return make_response(jsonify({
            "message": "incorrect or incomplete data provided."
        }), 404)


def join_pickup():

    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find(
        {"pickupId": request.headers["pickupId"]}
    )

    if pickupFound:

        checkHost = pickupCol.find({
            "hostId": request.headers["userId"]
        })

        if checkHost:

            return make_response(jsonify({
                "message": "you cannot join a pickup you have created."
            }))

        pickupCol.update_one({"pickupId": request.headers["pickupId"]},
                             {"$push": {"passengers.$.passengerId": request.headers["userId"]}})

        return make_response(jsonify({
            "message": "You have successfully joined the pickup."
        }))

    else:
        return make_response(jsonify({
            "message": "this pickup has not been found please try again."
        }))


def host_remove_passenger():
    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find(
        {"pickupId": request.headers["pickupId"]})

    if pickupFound:

        if pickupFound["hostId"] == request.headers["userId"]:
            pickupCol.update_one({"pickupId": request.headers["pickupId"]},
                                 {"$push": {"passengers.$.passengerId": request.headers["userId"]}})

            return make_response(jsonify({
                "message": "Passenger successfully removed."
            }))

        else:
            return make_response(jsonify({
                "message": "You are not the host of this pickup, only the host may remove another passenger."
            }))
    else:
        return make_response(jsonify({
            "message": "this pickup location has not been found."
        }))


def exit_pickup():

    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find(
        {"pickupId": request.headers["pickupId"]}
    )

    if pickupFound:

        checkHost = pickupCol.find({
            "hostId": request.headers["userId"]
        })

        if checkHost:

            return make_response(jsonify({
                "message": "host cannot leave their own pickup, please delete pickup instead."
            }))

        checkPassengerExists = pickupCol.find({
            "passengers.$.passengerId": request.headers["userId"]
        })

        if checkPassengerExists:

            pickupCol.update_one({"pickupId": request.headers["pickupId"]},
                                 {"$pull": {"passengers.$.passengerId": request.headers["userId"]}})

        else:
            return make_response(jsonify({
                "message": "Im sorry, you have not been found in this pickup point."
            }))


def get_pickup_points_for_user():

    pickupCol = Pickup._get_collection()

    pickupsFound = pickupCol.find(
        {"hostId": request.headers["userId"]}
    )

    if pickupsFound is not None:
        return make_response(jsonify({
            "message": "user has pickups hosted",
            "data": parse_json(pickupsFound)
        }))


def get_pickup_points_for_location():

    pickupCol = Pickup._get_collection()

    pickupsFound = pickupCol.find({"location": {"$within": {"$center": [[request.json["lat"], request.json["lng"]], 0.1]}}})
   
    if pickupsFound is not None:

        return make_response(jsonify({
                "message": "pickups in your area have been found",
                "data": parse_json(pickupsFound)
        }),201)
    else:
        return make_response(jsonify({
            "message": "no pickups have been found in this area."
        }),404)

def get_host_details():

    pickupCol = Pickup()._get_collection()

    pickupFound = pickupCol.find(
        {"pickupId":request.json["pickupId"],"hostId": request.json["hostId"]}
    )

    if pickupFound is not None: 

        userCol = User._get_collection()

        userFound = userCol.find_one({
            "userID": request.json["hostId"]
        })

        if userFound is not None:

            return make_response(jsonify({
                "message": "User profile has been found",
                "data": parse_json(userFound)
            }))
        else:
            return make_response(jsonify({
                "message": "user has not been found"
            }))

    else:
        return make_response(jsonify({
            "message": "a pickup has not been found associated with this user."
        }))
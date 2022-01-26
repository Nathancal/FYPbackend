import json
from mongoengine.errors import ValidationError
from app.model.pickup_model import Pickup
import uuid
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify


def create_pickup_point():

    try:
        print(request.json["hostId"])

        pickup = Pickup()
        pickup.pickupId = uuid.uuid4().hex
        pickup.hostId = request.json["hostId"]
        pickup.lat = request.json["lat"]
        pickup.lng = request.json["lng"]
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

    pickupFound = pickupCol.find(
        {"hostId": request.headers["userId"]}
    )

    if pickupFound is not None:
        return make_response(jsonify({
            "message": "user has pickups hosted",
            "data": parse_json(pickupFound)
        }))

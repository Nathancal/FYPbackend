import datetime
from itsdangerous import json
from mongoengine.errors import ValidationError
from pyparsing import empty
from app.model.pickup_model import Pickup
from app.model.user_model import User
import uuid
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify


def create_pickup_point():

    try:
        print(request.json["hostId"])

        eLat = request.json["eLat"]
        eLng = request.json["eLng"]

        rLat = request.json["rLat"]
        rLng = request.json["rLng"]
        embarkLocationObj = {
            'type': 'Point',
            'coordinates': [eLat, eLng]
        }

        returnLocationObj = {
            'type': 'Point',
            'coordinates': [rLat, rLng]
        }

        pickup = Pickup()
        pickup.pickupId = uuid.uuid4().hex
        pickup.hostId = request.json["hostId"]
        pickup.embarkLocation = parse_json(embarkLocationObj)
        pickup.returnLocation = parse_json(returnLocationObj)
        pickup.createdAt = datetime.datetime.utcnow()
        pickup.embarkAddress = request.json["embarkAddress"]
        pickup.returnAddress = request.json["returnAddress"]
        pickup.date = request.json["date"]
        pickup.time = request.json["time"]
        pickup.totalNumPassengers = request.json["totalNumPassengers"]

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

def check_user_is_passenger():

    pickupCol = Pickup._get_collection()

    checkPassengerExists = pickupCol.find_one({
            "pickupId": request.json["pickupId"]
                    })


    if checkPassengerExists is not None:

        for passenger in checkPassengerExists["passengers"]:

            if passenger["passengerId"] == request.json["userId"]:

                return make_response(jsonify({
                    "message": "user is a passenger in this pickup",
                    "isPassenger": True,
                    "data": parse_json(checkPassengerExists)
                }))
    else:
        return make_response(jsonify({
            "message": "user has not been found in this pickup.",
            "isPassenger": False
        }))
    

def join_pickup():

    pickupCol = Pickup._get_collection()

    pickupCheck = pickupCol.find_one({
        "pickupId": request.json["pickupId"],
    })

    if pickupCheck:

        if pickupCheck["passengers"]:

            for passenger in pickupCheck["passengers"]:

                if passenger["passengerId"] == request.json["userId"]:

                    return make_response(jsonify({
                        "message": "you have already joined this pickup."}
                    ), 409)
                else:

                    if len(pickupCheck["passengers"]) >= pickupCheck["totalNumPassengers"]:
                        return make_response(jsonify({
                            "message": "this pickup is full, please try another."
                        }))

                    joinPickup = pickupCol.update_one({
                        "pickupId": request.json["pickupId"],
                    },
                        {"$push": {
                            "passengers":
                            {"passengerId": request.json["userId"],
                             "date": datetime.datetime.utcnow()
                             }

                        }}, True)

                    return make_response(jsonify({
                        "message": "success!",
                    }), 201)

        else:

            joinPickup = pickupCol.update_one({
                "pickupId": request.json["pickupId"],
            },
                {"$push": {
                    "passengers":
                    {"passengerId": request.json["userId"],
                     "date": datetime.datetime.utcnow()
                     }
                }}, True)
            return make_response(jsonify({
                "message": "success!",
            }), 201)

    else:

        return make_response(jsonify({
            "message": "pickup not found",
        }), 404)


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
        {"pickupId": request.json["pickupId"]}
    )

    if pickupFound:

        if pickupFound["hostId"] == request.json["userId"]:

            return make_response(jsonify({
                "message": "host cannot leave their own pickup, please delete pickup instead."
            }))

        checkPassengerExists = pickupCol.find({
            "pickupId": request.json["pickupId"],
            "passengers.$.passengerId": request.json["userId"]
        })

        if checkPassengerExists:

            exitPickup = pickupCol.update_one({
                "pickupId": request.json["pickupId"],
            },
            {"$pull": {
                "passengers":
                {"passengerId": request.json["userId"] }}})
            
            return make_response(jsonify({
                "message": "you have successfully left the pickup."
            }))
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

    pickupsFound = pickupCol.find({"embarkLocation": {"$within": {"$center": [
                                  [request.json["lat"], request.json["lng"]], 0.1]}}})

    if pickupsFound is not None:

        return make_response(jsonify({
            "message": "pickups in your area have been found",
            "data": parse_json(pickupsFound)
        }), 201)
    else:
        return make_response(jsonify({
            "message": "no pickups have been found in this area."
        }), 404)

def get_passenger_details():

    userCol = User._get_collection()

    userFound = userCol.find({
        "userID": request.json["passengerId"]
    })

    if userFound:

        return make_response(jsonify({
            "message": "user details have been found",
            "data": parse_json(userFound)
        }))

    else: 
        return make_response(jsonify({
            "message": "user has not been found."
        }))

def get_host_details():

    pickupCol = Pickup()._get_collection()

    pickupFound = pickupCol.find(
        {"pickupId": request.json["pickupId"],
            "hostId": request.json["hostId"]}
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

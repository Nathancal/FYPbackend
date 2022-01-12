from mongoengine.errors import ValidationError
from app.model.pickup_model import Pickup
import uuid
from app.utility.parsejson_utility import parse_json
from flask import json, request, make_response, jsonify


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

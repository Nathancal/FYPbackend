from mongoengine.errors import ValidationError
from app.model.pickup_model import Pickup
import uuid
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify


def create_pickup_point():
    
    try:
        
        pickup = Pickup()
        pickup.pickupId = uuid.uuid4().hex
        pickup.hostId = request.json["hostId"]
        pickup.lat = request.json["latitude"]
        pickup.lng = request.json["longitude"]
        pickup.date = request.json["date"]
        pickup.address = request.json["address"]

        pickup.save()

        return make_response(jsonify({
            "message": "rendezvous successfully created!"
        }))
    except ValidationError as e:
        return make_response(jsonify({
            "message":"some fields may be empty please try again."
        }),404)

def get_pickup_point():


    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find_one(
        {"pickupId": request.json["pickupId"]}
    )

    if pickupFound is not None:
        return make_response(jsonify({
            "message": "rendezvous has been found",
            "data": parse_json(pickupFound)
        }))

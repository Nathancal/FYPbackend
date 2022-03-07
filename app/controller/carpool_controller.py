import uuid
from app.model.carpool_model import Carpool
from flask import request, make_response, jsonify


def initialise_carpool():

    carpool = Carpool()
    carpool.carpoolId = uuid.uuid4().hex
    carpool.firstPickupId = request.headers["embarkPickupId"]
    carpool.secondPickupId = request.headers["returnPickupId"]
    carpool.hostId = request.headers["hostId"]

    carpool.save()

    return make_response(jsonify({
        "message": "carpool successfully created."
    }))

def get_carpool_by_id():

    carpoolCol = Carpool._get_collection()

    carpoolFound = carpoolCol.find({
        "carpoolId": request.headers["carpoolId"]
    })

    if carpoolFound:

        return make_response(jsonify({
            "message": "carpool found",
            "data": carpoolFound
            }))

    else: 
        return make_response(jsonify({
            "message": "this carpool has not been found."
        }))

def get_carpools_for_host():

    carpoolCol = Carpool._get_collection()

    carpoolFound = carpoolCol.find({
        "hostId": request.headers["hostId"]
    })

    if carpoolFound:

        return make_response(jsonify({
            "message": "carpool found",
            "data": carpoolFound
            }))

    else: 
        return make_response(jsonify({
            "message": "this carpool has not been found."
        }))


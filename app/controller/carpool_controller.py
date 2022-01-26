import uuid
from app.model.carpool_model import Carpool
from flask import request, make_response, jsonify


def initialise_carpool():

    carpool = Carpool()
    carpool.carpoolId = uuid.uuid4().hex
    carpool.firstPickupId = request.headers["firstPickupId"]
    carpool.secondPickupId = request.headers["secondPickupId"]
    carpool.hostId = request.headers["hostId"]

    carpool.save()

    return make_response(jsonify({
        "message": "carpool successfully created."
    }))


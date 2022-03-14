import datetime
from flask import request, make_response, jsonify, session
from app.model.pickup_model import Pickup


def join_journey():

    pickupCollection = Pickup._get_collection()

    passengerId = request.json["userId"]
    userForename = request.json["userForename"]
    pickupId = request.json["pickupId"]
    joinedAt = datetime.datetime.utcnow()

    pickupFound = pickupCollection.find_one({
        'pickupId': pickupId
    })

    if pickupFound is not None:
        session['userId'] = passengerId
        session["journeyGroup"] = pickupId
        session['userForename'] = userForename

        print(session["journeyGroup"])

        for passenger in pickupFound["passengers"]:
            print(passenger["passengerId"])

            if passenger["passengerId"] == passengerId:

                passengerUpdate = {
                    'passengers.$.joinedAt': joinedAt,
                    'passengers.$.joined': True
                }

                pickupCollection.update_one({
                    'pickupId': pickupId,
                    'passengers.passengerId': passengerId
                }, {
                    '$set': passengerUpdate
                })

                return make_response(jsonify({
                    "joined": True,
                    "message": "you have successfully joined the journey."
                }))
        
        return make_response(jsonify({
            "message": "you cannot begin a journey you havent already joined."
        }))
    else: 
        return make_response(jsonify({
            "joined": False,
            "message": "this pickup has not been found"
        }))
import enum
from app.view.journey_routes import journeyBP
from app.view.user_routes import userBP
from app.view.pickup_routes import pickupBP
from app import app
from flask_socketio import SocketIO
import eventlet
from flask import request, session
from flask_socketio import emit, join_room

from app.model.pickup_model import Pickup

from app.utility.dbconnect_utility import DBConnect


async_mode = 'eventlet'


socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

app.wsgi_app = DBConnect(app.wsgi_app)


app.register_blueprint(userBP)
app.register_blueprint(pickupBP)
app.register_blueprint(journeyBP)

activeUsers = []

user = {}


@socketio.on('autocomplete')
def startJourney(message):

    emit('autocomplete ', {'isCompleted': message["completed"]},room=message["pickupId"])



@socketio.on('checkedin')
def checkedIn(message):

    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find_one({
        "pickupId": message["pickupId"]
    })

    if pickupFound is not None:

        for passenger in pickupFound["passengers"]:

            if passenger["passengerId"] == message["userId"]:

                if passenger["joined"] == True:

                    for index, user in enumerate(activeUsers):
                        print(user)
                        if user["userId"] == message["userId"]:
                            print("got HERE!")
                            user = {'userId': message["userId"],
                                          'pickupId': message["pickupId"],
                                          'joined': True}

                            activeUsers[index] = user

                            emit('checkedin', {'users': [activeUsers[index]]},
                                room=message["pickupId"])
                else:

                    print("ALL ELSE")
                    emit('checkedin', {'users': activeUsers},
                         room=message["pickupId"])


@socketio.on('joined')
def joined(message):

    pickupCol = Pickup._get_collection()

    userJoined = pickupCol.find_one({
        "pickupId": message["pickupId"]
    })

    if userJoined is not None:

        print("GETS level 2")

        for passenger in userJoined["passengers"]:

            print("level 3")

            if passenger["passengerId"] == message["userId"]:
                print("level 4") 

                for user in activeUsers:
                    print("level 5")

                    if message["userId"] == user["userId"]:
                        print("level 6")

                        emit('joined', {
                             'message': 'Already joined the pickup'})

                if message['userId'] not in activeUsers:
                    print("level 6")

                    user = {'userId': message["userId"],
                            'pickupId': message["pickupId"],
                            'joined': False}
                    activeUsers.append(user)

                journeyGroup = message["pickupId"]

                print("Pickup id: " + message["pickupId"])
                join_room(journeyGroup)

                emit('joined', {'msg': message["forename"] + ' has joined the pickup', 'userId': message["userId"],
                                'forename': message['forename'], 'users': activeUsers}, room=journeyGroup, broadcast=True)


if __name__ == '__main__':
    print('Server is running.....')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True,
                 keyfile='key.pem', certfile='cert.pem')

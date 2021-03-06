import enum
from app.view.journey_routes import journeyBP
from app.view.user_routes import userBP
from app.view.user_rating_routes import userRatingBP
from app.view.chat_routes import chatBP

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
app.register_blueprint(userRatingBP)
app.register_blueprint(chatBP)

activeUsers = []

user = {}


@socketio.on('checkedin')
def checkedIn(message):

    pickupCol = Pickup._get_collection()

    pickupFound = pickupCol.find_one({
        "pickupId": message["pickupId"]
    })

    if pickupFound is not None:

        if pickupFound["pickupStatus"] == 'completed':

            emit('checkedin', {'isComplete':True}, room=message["pickupId"])


        for passenger in pickupFound["passengers"]:

            if passenger["passengerId"] == message["userId"]:

                if passenger["joined"] == True:
                    user = {'userId': message["userId"],
                            'pickupId': message["pickupId"],
                            'joined': True} 

                    emit('checkedin', {'user': user, 'isComplete': False},
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

                if  message['userId'] in activeUsers:
                    journeyGroup = message["pickupId"]


                    emit('joined', {'msg': message["forename"] + ' has joined the pickup', 'userId': message["userId"],
                    'forename': message['forename'], 'users': activeUsers}, room=journeyGroup, broadcast=True)

                    print("level 6")
                else:
                    journeyGroup = message["pickupId"]


                    join_room(journeyGroup)

                    user = {'userId': message["userId"],
                            'forename': message["forename"],
                            'pickupId': message["pickupId"],
                            'joined': False}
                    activeUsers.append(user)

                    emit('joined', {'msg': message["forename"] + ' has joined the pickup', 'userId': message["userId"],
                    'forename': message['forename'], 'users': activeUsers}, room=journeyGroup, broadcast=True)


                print("Pickup id: " + message["pickupId"])

               


if __name__ == '__main__':
    print('Server is running.....')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True,
                 keyfile='key.pem', certfile='cert.pem')

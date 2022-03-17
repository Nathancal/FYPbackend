from ntpath import join
from app import app
from flask_socketio import SocketIO
import eventlet
from flask import request, session
from flask_socketio import emit, join_room

from app.model.pickup_model import Pickup



async_mode = 'eventlet'


socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

activeUsers = []

@socketio.on('hasJoined')
def checkUserJoined(message):

    pickupCol = Pickup._get_collection()
    userJoined = pickupCol.find_one({
        "pickupId": message["pickupId"]
    })

    if userJoined is not None:

        for passenger in userJoined["passengers"]:
        
            if passenger["passengerId"] == message["userId"]:

                if hasattr(passenger, 'joined'):
                    journeyGroup = message["pickupId"]


                    emit('hasJoined', { 'userId':message["userId"]}, broadcast=True)
            


@socketio.on('joined')
def joined(message):

    pickupCol = Pickup._get_collection()

    userJoined = pickupCol.find_one({
        "pickupId": message["pickupId"]
    })

    if userJoined is not None:

        for passenger in userJoined["passengers"]:
        
            if passenger["passengerId"] == message["userId"]:

                if hasattr(passenger, 'joined'):

                      if hasattr(activeUsers, 'userId'):
                        if message['userId'] not in activeUsers['userId']:
                            activeUsers.append({
                                'userId': message['userId'],
                                'forename': message['forename']
                            })
                        else:
                            activeUsers.append({
                                'userId': message['userId'],
                                'forename': message['forename']
                            })

                        journeyGroup = message["pickupId"]
  
                        

                        print("Pickup id: " + message["pickupId"])
                        join_room(journeyGroup)

                        emit('joined', {'msg': message["forename"] + ' has joined the pickup', 'userId': message["userId"],
                            'forename': message['forename'], 'users': activeUsers}, room=journeyGroup, broadcast=True)


if __name__ == '__main__':
    print('Server is running.....')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True,
                 keyfile='key.pem', certfile='cert.pem')

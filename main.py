from app import app
from flask_socketio import SocketIO
import eventlet
from flask import session
from flask_socketio import emit, join_room


async_mode = 'eventlet'


socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

activeUsers = []


@socketio.on('joined')
def joined(message):


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

from app import app
from flask_socketio import SocketIO
import eventlet
from flask import session
from flask_socketio import emit, join_room




async_mode = 'eventlet'



socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

@socketio.on('joined')
def joined(message):
    journeyGroup = session.get('journeyGroup')
    join_room(journeyGroup)
    emit('status', {'msg': message + ' has joined the pickup'}, room=journeyGroup)



if __name__ == '__main__':
    print('Server is running.....')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, keyfile='key.pem', certfile='cert.pem')
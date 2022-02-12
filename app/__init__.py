from flask import Flask
from flask_cors import CORS
from pymongo import GEO2D


from app.utility.dbconnect_utility import DBConnect 

app = Flask(__name__)
CORS(app)

app.wsgi_app = DBConnect(app.wsgi_app)

from app.view.pickup_routes import pickupBP
from app.view.user_routes import userBP

app.register_blueprint(userBP)
app.register_blueprint(pickupBP)

if __name__ == '__main__':
    context = ('local.crt', 'local.key')#certificate and key files
    app.run(debug=True, ssl_context=context)
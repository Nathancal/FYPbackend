from flask import Flask
from flask_cors import CORS

from app.utility.dbconnect_utility import DBConnect 

app = Flask(__name__)
CORS(app)

app.wsgi_app = DBConnect(app.wsgi_app)

from app.view.pickup_routes import pickupBP
from app.view.user_routes import userBP

app.register_blueprint(userBP)
app.register_blueprint(pickupBP)
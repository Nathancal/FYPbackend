from distutils.log import debug
from flask import Flask
from flask_cors import CORS
from pymongo import GEO2D


from app.utility.dbconnect_utility import DBConnect 



app = Flask(__name__)
app.secret_key = 'SecretsSecretSecrets!!!'

CORS(app)

app.wsgi_app = DBConnect(app.wsgi_app)



from app.view.pickup_routes import pickupBP
from app.view.user_routes import userBP
from app.view.journey_routes import journeyBP

app.register_blueprint(userBP)
app.register_blueprint(pickupBP)
app.register_blueprint(journeyBP)




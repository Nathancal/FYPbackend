from distutils.log import debug
from flask import Flask
from flask_cors import CORS
from pymongo import GEO2D

app = Flask(__name__)
app.secret_key = 'SecretsSecretSecrets!!!'

CORS(app)






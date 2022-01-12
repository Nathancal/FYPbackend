import datetime
from mongoengine.errors import NotUniqueError, ValidationError
from app.model.user_model import User
import uuid
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify
import jwt
import bcrypt

def signup():

    try:

        password = str(request.json["password"])

        hash = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10)))
        
        splitHash = hash.split("'", 3)

        user = User()
        user.userID = uuid.uuid4().hex
        user.email = request.json["email"]
        user.password = str(splitHash[1])
        user.firstName = request.json["firstName"]
        user.lastName = request.json["lastName"]

        user.save()

        userResponseObj = User._get_collection()

        return make_response(jsonify(
            {"message": "successfully created an account.",
            "data": parse_json(userResponseObj.find_one({'email': request.json["email"]}))}
        ),201)

    except NotUniqueError as e:
        return make_response(jsonify({
            "message":"A user with this email already exists, please login."
        }),409)

    except ValidationError as e:
        return make_response(jsonify({
            "messaage":"One of the required fields has invalid or missing data."
        }))

def login():

        user = User._get_collection()

        checkEmailExists = user.find_one({'email': request.json["email"]})

        if checkEmailExists is not None:

            password = str(request.json["password"])
            crossRefPassword = bytes(checkEmailExists["password"], 'UTF-8')

            if bcrypt.checkpw(bytes(password, 'UTF-8'), crossRefPassword):

                token = jwt.encode({
                    'user': checkEmailExists["email"],
                    'admin': checkEmailExists["admin"],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                },'TestSecret', algorithm="HS256")

                return make_response(jsonify({
                    "message": "successfully logged in",
                    "token": token,
                    "userId": parse_json(checkEmailExists["userID"]),
                    "firstName": parse_json(checkEmailExists["firstName"])
                }))
            
            else:
                return make_response(jsonify({
                    "message": "password is incorrect."
                }))
        else: 
            return make_response(jsonify({
                "message": "Email does not exist, please create an account"
            }))
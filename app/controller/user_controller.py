import datetime
from importlib.metadata import requires
from itsdangerous import json
from mongoengine.errors import NotUniqueError, ValidationError
from app.model.transaction_model import Transactions
from app.model.user_model import User
import uuid
from app.model.user_rating_model import userRating
from app.utility.parsejson_utility import parse_json
from flask import request, make_response, jsonify
import jwt
import bcrypt


def signup():

    try:

        password = str(request.json["password"])

        hash = str(bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt(rounds=10)))

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
        ), 201)

    except NotUniqueError as e:
        return make_response(jsonify({
            "message": "A user with this email already exists, please login."
        }), 409)

    except ValidationError as e:
        return make_response(jsonify({
            "messaage": "One of the required fields has invalid or missing data."
        }),403)


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
            }, 'TestSecret', algorithm="HS256")

            return make_response(jsonify({
                "message": "successfully logged in",
                "token": token,
                "userId": parse_json(checkEmailExists["userID"]),
                "firstName": parse_json(checkEmailExists["firstName"])
            }), 201)

        else:
            return make_response(jsonify({
                "message": "password is incorrect."
            }), 404)
    else:
        return make_response(jsonify({
            "message": "Email does not exist, please create an account"
        }), 404)


def get_user_miles():

    user = User._get_collection()

    findUser = user.find_one({'userID': request.json["userID"]})

    if findUser is not None:

        return make_response(jsonify({
            "message": "miles returned successfully",
            "miles": findUser["totalMiles"]
        }),201)
    else:
        return make_response(jsonify({
            "message": "user has not been found."
        }),404)


def update_user_miles():

    user = User._get_collection()

    findUser = user.find_one({'userID': request.json["userID"]})

    if findUser is not None:

        try:

            updateMiles = user.update_one({
                "userID": request.json["userID"],
            },
            {"$set": {"totalMiles": request.json["updateTotalMiles"]}})

            return make_response(jsonify({
            "message": "miles successfully updated."
        }),200)

        except Exception as e:
            return make_response(jsonify({
                "message": "error with update.",
                "error": e
            }),403)
        
    else:
        
        return make_response(jsonify({
            "message": "user has not been found"
        }),404) 

def generate_transaction():

    try: 
        userToTransact = User.objects.get(userID=request.json["userId"])

        trans = Transactions()
        trans.milestransId = uuid.uuid4().hex
        trans.isHost = request.json["isHost"]
        trans.pickupId = request.json["pickupId"]
        trans.totalMilesTravelled = request.json["milesTravelled"]
        trans.totalNumPassengers = request.json["totalNumPassengers"]
        trans.embarkAddress = request.json["embarkAddress"]
        trans.returnAddress = request.json["returnAddress"]
        trans.completedAt = datetime.datetime.utcnow()

        userToTransact.transactions.append(trans)
        userToTransact.save()

        return make_response(jsonify({
            "message": "transaction successfully completed"
        }),200)



    except Exception as e:
        return make_response(jsonify({
            "message": "an error has occured adding the transaction",
            "error": e
        }), 401)

def get_all_transactions():

    try:
        
        user = User._get_collection()

        findUser = user.find_one({'userID': request.json["userID"]})

        if findUser is not None:
            
            if findUser["transactions"] is not None:

                return make_response(jsonify({
                    "message": "transactions list successfully found.",
                    "data": findUser["transactions"]
                }),200)
            else:
                return make_response(jsonify({
                    "message":"no transactions have been found associated with this account."
                }),404)
        else:
            return make_response(jsonify({
                "message": "this user has not been found."
            }),404)
    except Exception as e:
        return make_response(jsonify({
            "message": "an unknown exception has occured."
        }),403)
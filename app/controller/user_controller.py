import datetime
from importlib.metadata import requires
from mongoengine.errors import NotUniqueError, ValidationError
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
            }),404)
    else:
        return make_response(jsonify({
            "message": "Email does not exist, please create an account"
        }),404)

def review_user():

    checkUser = User._get_collection()

    userToReview = request.headers["userToReviewId"]

    userFound = checkUser.find_one({
        "userId": request.headers["userToReviewId"]
    })

    if userFound:

        try:

            newRating = userRating()
            newRating.ratingId = uuid.uuid4().hex
            newRating.userPostedId = request.headers["userId"]
            newRating.userToReviewId = userToReview
            newRating.score = request.json["score"]
            newRating.comment = request.json["comment"]
            newRating.date = datetime.datetime.utcnow()

            set_user_rating(userToReview)

        except ValidationError:
            return make_response(jsonify({
                "message": "some information may be missing please try again."
            }))

        return make_response(jsonify({
            "message": "your review has successfully been created"
        }))
    else:
        return make_response(jsonify({
            "message": "this user has not been found, please try again."
        }))

def set_user_rating(userId):

    userCol = User._get_collection()

    userScores = userCol.aggregate([
        {"$match": {"userId": userId}},
        {"$unwind": "reviews"},
        {"$group": {"averageScore": {"$avg": "reviews.score"}}}
    ])

    userCol.update_one({
        "userId": userId
    },{"$set": {
        "score": userScores["averageScore"]
    }})

def get_user_rating():

    userCol = User._get_collection()

    userScore = userCol.find_one({
        "userId": request.headers["userId"]
    },{ "_id": 0, "avgScore": 1 })  

    if userScore:

        return make_response(jsonify({
            "message": "user rating found.",
            "data": userScore
        }))

    else: 

        return make_response(jsonify({
            "message": "user has not been found"
        }))




import uuid
from flask import request, make_response, jsonify
from itsdangerous import json
from app.model.user_model import User
from app.model.user_rating_model import userRating


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


def rate_user():

    userToRate = User.objects.get(userID=request.json["userId"])


    if userToRate is not None:

        userReview = userRating()

        userReview.ratingId = uuid.uuid4().hex
        userReview.score = request.json["score"]
        userReview.comment = request.json["comment"]
        userReview.userPostedId = request.json["userId"]
        userReview.userToReviewId = request.json["userUnderReviewId"]

        userToRate.reviews.append(userReview)

        userToRate.save()

        return make_response(jsonify({
            "message": "user has been successfully reviewed."
        }))

    else:
        return make_response(jsonify({
            "message": "user has not been found."
        }))


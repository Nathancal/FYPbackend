
from asyncio.windows_events import NULL
import uuid
from flask import request, make_response, jsonify
from itsdangerous import json
from app.model.user_model import User
from app.model.user_rating_model import userRating


def set_user_rating():

    userCol = User._get_collection()

    userScores = userCol.aggregate([
        {"$match": {"userID": request.json["userId"]}},
        {"$unwind": "$reviews"},
        {"$group": {"_id":NULL, "averageScore": { "$avg": "$reviews.score"}}}
    ])

    scores = list(userScores)
 
    print(scores)

    try:

        userCol.update_one({
            "userID": request.json["userId"]
        }, {"$set": {
            "avgScore": scores[0]["averageScore"]
        }})

        return make_response(jsonify({
            "message": "user rating successfully recalculated."
        }))
    except Exception as e:
        return make_response(jsonify({
            "message": "a problem has occoured updating the user rating."
        }))




def get_user_rating():

    userCol = User._get_collection()

    userScore = userCol.find_one({
        "userId": request.headers["userId"]
    }, {"_id": 0, "avgScore": 1})

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

    userToRate = User.objects.get(userID=request.json["userUnderReviewId"])

    if userToRate is not None:

        try:

            userReview = userRating()

            userReview.ratingId = uuid.uuid4().hex
            userReview.score = request.json["score"]
            userReview.comment = request.json["comment"]
            userReview.userPostedId = request.json["userId"]

            userToRate.reviews.append(userReview)

            userToRate.save()

            return make_response(jsonify({
                "message": "user has been successfully reviewed."
            }),201)
        except Exception as e:

            return make_response(jsonify({
                "message": "An unknown error has occoured please try again."
            }),403)

    else:
        return make_response(jsonify({
            "message": "user has not been found."
        }),404)

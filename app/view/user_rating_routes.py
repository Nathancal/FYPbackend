from flask.blueprints import Blueprint
from app.controller.user_rating_controller import rate_user, set_user_rating, get_user_rating

userRatingBP = Blueprint('userRatings', __name__, url_prefix='/api/v1/userrating')

@userRatingBP.route("/rateuser", methods=["GET", "POST"])
def rate_a_user():
    return rate_user()

@userRatingBP.route("/setscore", methods=["GET", "POST"])
def update_score():
    return set_user_rating()

@userRatingBP.route("/getscore", methods=["GET", "POST"])
def find_user_score():
    return get_user_rating()
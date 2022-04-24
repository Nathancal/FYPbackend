from flask.blueprints import Blueprint
from app.controller.user_rating_controller import rate_user

userRatingBP = Blueprint('userRatings', __name__, url_prefix='/api/v1/user')

@userRatingBP.route("/rateuser", methods=["GET", "POST"])
def rate_a_user():
    return rate_user()
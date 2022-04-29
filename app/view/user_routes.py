from flask.blueprints import Blueprint
from app.controller.user_controller import get_user_reviews, get_user_info, get_all_transactions, generate_transaction, signup, login, get_user_miles, update_user_miles

userBP = Blueprint('user', __name__, url_prefix='/api/v1/user')

@userBP.route("/signup", methods=["POST"])
def create_account():
    return signup()

@userBP.route("/login", methods=["POST"])
def loginUser():
    return login()

@userBP.route("/getmiles", methods=["POST","GET"])
def getMiles():
    return get_user_miles()

@userBP.route("/updatemiles", methods=["POST", "GET"])
def updateMiles():
    return update_user_miles()

@userBP.route("/generatetransaction", methods=["POST", "GET"])
def gen_transaction():
    return generate_transaction()

@userBP.route("/gettransactions", methods=["POST", "GET"])
def get_transaction_for_user():
    return get_all_transactions()


@userBP.route("/getuserinfo", methods=["POST", "GET"])
def get_info_for_user():
    return get_user_info()

@userBP.route("/getuserreviews", methods=["POST", "GET"])
def get_reviews_for_user():
    return get_user_reviews()
from flask.blueprints import Blueprint
from app.controller.user_controller import signup, login, get_user_miles, update_user_miles

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
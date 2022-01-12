from flask.blueprints import Blueprint
from app.controller.user_controller import signup, login

userBP = Blueprint('user', __name__, url_prefix='/api/v1/user')

@userBP.route("/signup", methods=["POST"])
def create_account():
    return signup()

@userBP.route("/login", methods=["POST"])
def loginUser():
    return login()
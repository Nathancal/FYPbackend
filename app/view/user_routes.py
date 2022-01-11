from flask.blueprints import Blueprint

userBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@userBP.route("/signup", methods=["POST"])
def create_account():
    pass

@userBP.route("/login", methods=["GET"])
def login():
    pass
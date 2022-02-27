import imp
from flask.blueprints import Blueprint
from app.controller.carpool_controller import initialise_carpool


carpoolBP = Blueprint('carpool', __name__, url_prefix='/api/v1/carpool')

@carpoolBP.route("/initcarpool", methods=["POST"])
def create_carpool():
    return initialise_carpool()

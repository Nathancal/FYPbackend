from flask.blueprints import Blueprint
from app.controller.pickup_controller import create_pickup_point

pickupBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@pickupBP.route("/create", methods=["POST"])
def create_rendezvous():
    create_pickup_point()
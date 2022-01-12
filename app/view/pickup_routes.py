from flask.blueprints import Blueprint
from app.controller.pickup_controller import create_pickup_point, get_pickup_points_for_user

pickupBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@pickupBP.route("/create", methods=["POST"])
def create_rendezvous():
    return create_pickup_point()

@pickupBP.route("/userhostedpickups", methods=["GET"])
def get_rendezvous_for_user():
    return get_pickup_points_for_user()
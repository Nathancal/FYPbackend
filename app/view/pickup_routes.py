from ntpath import join
from flask.blueprints import Blueprint
from app.controller.pickup_controller import create_pickup_point, get_pickup_points_for_user, get_pickup_points_for_location, join_pickup, get_host_details

pickupBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@pickupBP.route("/create", methods=["POST"])
def create_rendezvous():
    return create_pickup_point()

@pickupBP.route("/joinpickup", methods=["POST"])
def join_rendezvous():
    return join_pickup()

@pickupBP.route("/userhostedpickups", methods=["GET"])
def get_rendezvous_for_user():
    return get_pickup_points_for_user()

@pickupBP.route("/pickupsatlocation", methods=["GET", "POST"])
def get_rendezvous_at_location():
    return get_pickup_points_for_location()

@pickupBP.route("/gethostdetails", methods=["POST"])
def get_host_info():
    return get_host_details()
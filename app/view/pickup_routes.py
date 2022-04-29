from flask.blueprints import Blueprint
from app.controller.pickup_controller import get_pickup_user_passenger, get_pickup_details, create_pickup_point, get_pickup_points_for_user, check_user_is_passenger, get_pickup_points_for_location, join_pickup, get_host_details, exit_pickup, get_passenger_details, complete_pickup

pickupBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@pickupBP.route("/create", methods=["POST"])
def create_rendezvous():
    return create_pickup_point()

@pickupBP.route("/exitpickup", methods=["POST", "PUT"])
def exit_rendezvous():
    return exit_pickup()

@pickupBP.route("/completepickup", methods=["POST","GET"])
def complete_route():
    return complete_pickup()

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

@pickupBP.route("/getpassengerdetails", methods=["POST","GET"])
def get_passenger_dets():
    return get_passenger_details()

@pickupBP.route("/checkuserpassenger", methods=["POST","GET"])
def check_if_user_is_passenger():
    return check_user_is_passenger()

@pickupBP.route("/getpickupdetails", methods=["POST","GET"])
def get_pickup_data():
    return get_pickup_details()

@pickupBP.route("/getpickupsuserpassenger", methods=["POST","GET"])
def get_pickups_user_passeng():
    return get_pickup_user_passenger()
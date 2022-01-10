from flask.blueprints import Blueprint

pickupBP = Blueprint('pickup', __name__, url_prefix='/api/v1/pickup')

@pickupBP.route("/create", methods=["POST"])
def create_rendezvous():
    pass
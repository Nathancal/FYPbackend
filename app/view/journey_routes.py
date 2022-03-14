from flask.blueprints import Blueprint
from flask import session, request

from app.controller.journey_controller import join_journey



journeyBP = Blueprint('journey', __name__, url_prefix='/api/v1/journey')

@journeyBP.route('/join', methods=['GET','POST'])
def journey_join():
    return join_journey()

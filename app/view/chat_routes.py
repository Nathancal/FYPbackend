from flask.blueprints import Blueprint
from flask import session, request

from app.controller.chat_controller import create_chat, get_all_chats_for_user,check_chat_exist
from app.controller.message_controller import create_message


chatBP = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

@chatBP.route('/createchat', methods=['GET','POST'])
def create():
    return create_chat()

@chatBP.route('/getchatsuser', methods=['GET','POST'])
def get_chats_user():
    return get_all_chats_for_user()

@chatBP.route('/checkchatexists', methods=['GET','POST'])
def check_user_chat():
    return check_chat_exist()

@chatBP.route('/createmessage', methods=['GET','POST'])
def add_message():
    return create_message()



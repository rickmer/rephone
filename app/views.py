from flask import Blueprint, request
from .calls import make_call, dispatch
main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return make_call(request)


@main.route('/call', methods=['POST'])
def call():
    return make_call(request)


@main.route('/dispatch', methods=['POST'])
def dispatch():
    return dispatch()

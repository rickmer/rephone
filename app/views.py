from flask import Blueprint, request
from .calls import make_call, make_outbound_call
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return make_call(request)


@main.route('/outbound', methods=['GET'])
def outbound():
    return make_outbound_call()

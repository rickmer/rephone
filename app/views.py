from flask import Blueprint, request, Response
from .calls import make_call, make_outbound_call
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return make_call(request)


@main.route('/<id_campaign>', methods=['GET', 'POST'])
def campaign(id_campaign):
    return make_call(request, id_campaign)


@main.route('/embedded/<id_campaign>', methods=['GET', 'POST'])
def embedded_campaign(id_campaign):
    return make_call(request, id_campaign, embedded=True)


@main.route('/outbound/<record_id>', methods=['POST'])
def outbound(record_id):
    return make_outbound_call(record_id, request)


@main.route('/outbound/status/', methods=['POST'])
def status():
    print(request.values)
    return Response(status=200)

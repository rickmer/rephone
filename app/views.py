from flask import Blueprint, request
from .calls import make_call, make_outbound_call
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return make_call(request)


@main.route('/<id_campaign>', methods=['GET', 'POST'])
def campaign(id_campaign):
    return make_call(request, id_campaign)


@main.route('/<id_campaign>/<respondent_number>')
def campaign_respondent(id_campaign, respondent_number):
    return make_call(request, id_campaign, respondent_number)


@main.route('/outbound/<record_id>', methods=['POST'])
def outbound(record_id):
    return make_outbound_call(record_id)

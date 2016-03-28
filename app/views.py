from flask import Blueprint, request, Response
from .calls import make_outbound_call, get_call_widget, post_call_widget
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return get_call_widget(request)
    elif request.method == 'POST':
        return post_call_widget(request)


@main.route('/<id_campaign>', methods=['GET', 'POST'])
def campaign(id_campaign):
    if request.method == 'GET':
        return get_call_widget(request, id_campaign)
    elif request.method == 'POST':
        return post_call_widget(request, id_campaign)


@main.route('/embedded/<id_campaign>', methods=['GET', 'POST'])
def embedded_campaign(id_campaign):
    if request.method == 'GET':
        return get_call_widget(request, id_campaign, embedded=True)
    elif request.method == 'POST':
        return post_call_widget(request, id_campaign, embedded=True)


@main.route('/outbound/<record_id>', methods=['POST'])
def outbound(record_id):
    return make_outbound_call(record_id)


@main.route('/outbound/status/', methods=['POST'])
def status():
    from .abuse.calls import abuse_detected
    abuse_detected(phone_number=request.values['To'],
                   duration=request.values['CallDuration'])
    return Response(status=200)

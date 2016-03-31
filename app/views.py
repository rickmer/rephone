from flask import Blueprint, request, Response, redirect, abort
from .calls import make_outbound_call, get_call_widget, post_call_widget
from .abuse.client import is_blocked
main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return redirect('/1', 303)


@main.route('/<id_campaign>', methods=['GET', 'POST'], defaults={'template': ''})
@main.route('/<template>/<id_campaign>', methods=['GET', 'POST'])
def campaign(id_campaign, template):
    embedded_template = False
    if template == 'embedded':
        embedded_template = True
    if request.method == 'GET':
        return get_call_widget(request, id_campaign, embedded=embedded_template)
    elif request.method == 'POST':
        if is_blocked(request):
            return abort(429)
        return post_call_widget(request, id_campaign, embedded=embedded_template)


@main.route('/outbound/<record_id>', methods=['POST'])
def outbound(record_id):
    return make_outbound_call(record_id)


@main.route('/outbound/status/', methods=['POST'])
def status():
    from .abuse.calls import abuse_detected
    abuse_detected(phone_number=request.values['To'],
                   duration=request.values['CallDuration'])
    return Response(status=200)

from flask import render_template, flash, url_for, current_app, abort
from .models import Respondent, Campaign, Audience
from .forms import CallForm
from .abuse.calls import abuse_detected
from twilio import twiml
from twilio.rest import TwilioRestClient
from operator import attrgetter


def post_call_widget(request, id_campaign=1, embedded=False):
    """
    Render a call page due to a post request.
    :param request: a flask request object.
    :param id_campaign: an campaign id.
    :param embedded: True if embed template is supposed to be rendered.
    :return: flask response.
    """
    form = CallForm(request.form)
    campaign = Campaign().query.filter_by(id=id_campaign).first()
    if campaign is None:
        return abort(404)
    if embedded:
        template = 'callform/callform_embedded.html'
    else:
        template = 'callform/callform.html'
    if form.validate_on_submit():
        record = Respondent().query.filter_by(id=form.id_mdb.data).first()
        tel_mdb = record.phone
        tel_caller = form.phone_number.data
        if abuse_detected(phone_number=tel_caller):
            flash('I’m sorry Dave, I’m afraid I can’t do that.', category='warning')
            return render_template(template, record=record, form=form, campaign=campaign)
        if not initiate_call(record_id=form.id_mdb.data,
                             tel_caller=tel_caller,
                             audience_id=campaign.id_audience,
                             campaign_id=id_campaign,
                             request=request):
            flash('something went wrong', category='warning')
            return render_template(template, record=record, form=form, campaign=campaign)
        else:
            flash('dispatching call from ' + tel_caller + ' to ' + tel_mdb, category='info')
            return render_template(template, record=record, form=form, campaign=campaign)
    else:
        record = Respondent().query.filter_by(id=form.id_mdb.data).first()
        return render_template(template, record=record, form=form, campaign=campaign)


def get_call_widget(request, id_campaign=1, embedded=False):
    """
    Render a call page due to a get request.
    :param request: a flask request object.
    :param id_campaign: an campaign id.
    :param embedded: True if embed template is supposed to be rendered.
    :return: flask response.
    """
    form = CallForm(request.form)
    campaign = Campaign().query.filter_by(id=id_campaign).first()
    if campaign is None:
        return abort(404)
    if embedded:
        template = 'callform/callform_embedded.html'
    else:
        template = 'callform/callform.html'
    audience = Audience().query.filter_by(id=campaign.id_audience).first()
    random_id = current_app.random.get_random_value(campaign.id_audience)
    record = sorted(audience.respondents, key=attrgetter('id'))[random_id]
    return render_template(template, record=record, form=form, campaign=campaign)


def initiate_call(record_id, tel_caller, audience_id, campaign_id):
    """
    Dispatch a call to the user provided Phone number.
    :param record_id: if of the respondent to finally receive the call.
    :param tel_caller: phone number of the user.
    :param audience_id: the id of the audience whoms randomness needs to be biased.
    :param campaign_id: the id of the campaign to log statistics for.
    :return: True iff call was successfully dispatched.
    """
    callback_uri = url_for('.outbound',
                           _external=True,
                           _scheme='https',
                           record_id=str(record_id))

    status_uri = url_for('.status',
                         _external=True,
                         _scheme='https',
                         id_campaign=str(campaign_id))

    try:
        twilio_client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'],
                                         current_app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        current_app.logger.error(e)
        return False

    try:
        twilio_client.calls.create(from_=current_app.config['TWILIO_CALLER_ID'],
                                   to=tel_caller,
                                   url=callback_uri,
                                   method='POST',
                                   status_callback=status_uri,
                                   status_callback_method='POST',
                                   status_callback_events=['completed'])

    except Exception as e:
        current_app.logger.error(e)
        return False
    current_app.random.add_sample(audience_id=audience_id, respondent_id=record_id)
    return True


def make_outbound_call(record_id):
    """
    Twilio callback for a call to get connected to the respective respondent.
    :param record_id: id of the respondent
    :return: flask response (XML).
    """

    response = twiml.Response()

    record = Respondent().query.filter_by(id=record_id).first()
    if record is None:
        return abort(404)

    response.say("Hello, thanks for your Participation. We will now connect you to your Member of Parliament.",
                 voice='alice')

    if current_app.config['demo_mode']:
        response.hangup()
    with response.dial() as dial:
        if current_app.config['TWILIO_TEST_NUMBER']:
            dial.number(current_app.config['TWILIO_TEST_NUMBER'])
        else:
            dial.number(record.phone)

    return str(response)

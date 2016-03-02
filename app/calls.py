from flask import render_template, flash, url_for, current_app, abort
from .models import Respondent, Campaign, Audience
from .forms import CallForm
from twilio import twiml
from twilio.rest import TwilioRestClient
from random import randint
from operator import attrgetter


def make_call(request, id_campaign=1):
    form = CallForm(request.form)
    campaign = Campaign().query.filter_by(id=id_campaign).first()
    if campaign is None:
        return abort(404)
    if request.method == 'GET':
        audience = Audience().query.filter_by(id=campaign.id_audience).first()
        random_id = randint(0, 750)
        record = sorted(audience.respondents, key=attrgetter('id'))[random_id]
        return render_template('callform.html', record=record, form=form, campaign=id_campaign)
    elif request.method == 'POST':
        if form.validate_on_submit():
            record = Respondent().query.filter_by(id=form.id_mdb.data).first()
            tel_mdb = record.phone
            tel_caller = form.phone_number.data
            if not initiate_call(record_id=form.id_mdb.data, tel_caller=tel_caller):
                flash('something went wrong', category='warning')
                return render_template('callform.html', record=record, form=form, campaign=id_campaign)
            else:
                flash('dispatching call from ' + tel_caller + ' to ' + tel_mdb, category='info')
                return render_template('callform.html', record=record, form=form, campaign=id_campaign)
        else:
            record = Respondent().query.filter_by(id=form.id_mdb.data).first()
            return render_template('callform.html', record=record, form=form, campaign=id_campaign)


def make_outbound_call(record_id):

    response = twiml.Response()

    record = Respondent().query.filter_by(id=record_id).first()
    if record is None:
        return abort(404)

    response.say("Hallo! Wir verbinden Dich jetzt. Danke für Deine Zeit.",
                 voice='alice',
                 language='de')
    
    if current_app.config['demo_mode']:
        response.hangup()
    else:
        with response.dial() as dial:
            dial.number(record.telefon_nr)

    return str(response)


def initiate_call(record_id, tel_caller):
    callback_uri = url_for('.outbound', _external=True, _scheme='https', record_id=str(record_id))
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
                                   method='POST')
    except Exception as e:
        current_app.logger.error(e)
        return False
    return True

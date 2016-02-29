from flask import render_template, flash, url_for, current_app, abort
from .models import MitgliedDesBundestages
from .forms import CallForm
from twilio import twiml
from twilio.rest import TwilioRestClient


def make_call(request):
    form = CallForm(request.form)
    if request.method == 'GET':
        from random import randint
        random_id = randint(1, 631)
        record = MitgliedDesBundestages().query.filter_by(id=random_id).first()
        return render_template('callform.html', record=record, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            record = MitgliedDesBundestages().query.filter_by(id=form.id_mdb.data).first()
            tel_mdb = record.telefon_nr
            tel_caller = form.phone_number.data
            callback_uri = url_for('.outbound', _external=True, _scheme='https', record_id=str(record.id))
            try:
                twilio_client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'],
                                                 current_app.config['TWILIO_AUTH_TOKEN'])
            except Exception as e:
                current_app.logger.error(e)
                flash('something went wrong', category='warning')
                return render_template('callform.html', record=record, form=form)

            try:
                twilio_client.calls.create(from_=current_app.config['TWILIO_CALLER_ID'],
                                           to=tel_caller,
                                           url=callback_uri,
                                           method='POST')
            except Exception as e:
                current_app.logger.error(e)
                flash('something went wrong', category='warning')
                return render_template('callform.html', record=record, form=form)

            flash('dispatching call from ' + tel_caller + ' to ' + tel_mdb, category='info')
            return render_template('callform.html', record=record, form=form)
        else:
            record = MitgliedDesBundestages().query.filter_by(id=form.id_mdb.data).first()
            return render_template('callform.html', record=record, form=form)


def make_outbound_call(record_id):

    response = twiml.Response()

    record = MitgliedDesBundestages().query.filter_by(id=record_id).first()
    if record is None:
        return abort(404)

    response.say("Hallo! Wir verbinden Dich jetzt. Danke für Deine Zeit.",
                 voice='alice',
                 language='de')

    with response.dial() as dial:
        dial.number(record.telefon_nr)

    return str(response)



from flask import render_template, flash, url_for, current_app
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
                                           url=url_for('.outbound', _external=True, _scheme='https'))
            except Exception as e:
                current_app.logger.error(e)
                flash('something went wrong', category='warning')
                return render_template('callform.html', record=record, form=form)

            flash('dispatching call from ' + tel_caller + ' to ' + tel_mdb, category='info')
            return render_template('callform.html', record=record, form=form)
        else:
            flash('Something went wrong', category='warning')
            record = MitgliedDesBundestages().query.filter_by(id=form.id_mdb.data).first()
            return render_template('callform.html', record=record, form=form)


def make_outbound_call():
    response = twiml.Response()

    response.say("Hallo! Wir verbinden Dich jetzt. Danke für Deine Zeit.",
                 voice='alice',
                 language='de')
    response.hangup()
    return str(response)



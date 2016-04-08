from flask import current_app
from app.models import db, PossibleAbuses
from hashlib import sha256
from datetime import date


def abuse_detected(phone_number, duration=None, persist=False):
    """
    :param phone_number: a phone number to add to the abuse tracker.
    :param duration: the duration of the call.
    :param persist: iff persist is set to True abuse flag will be set permanently
    :return: true iff abuse is likely
    """

    hashed_phone_number = sha256(bytes(str(phone_number), 'utf-8')).hexdigest()
    short_calls = 0
    if duration is not None and int(duration) <= current_app.config['SHORT_CALL_THRESHOLD']:
        short_calls = 1

    abuse_case = PossibleAbuses().query.filter_by(id=hashed_phone_number).first()
    if abuse_case is None:
        abuse_case = PossibleAbuses()
        abuse_case.id = hashed_phone_number
        abuse_case.short_calls = 0 + short_calls
        abuse_case.date = date.today()
        abuse_case.persistent = persist
        db.session.add(abuse_case)
    elif abuse_case.date == date.today():
        abuse_case.short_calls += short_calls
    else:
        abuse_case.date = date.today()
        abuse_case.short_calls = short_calls
    if persist:
        abuse_case.persistent = True
    db.session.commit()

    if abuse_case.persistent or \
       abuse_case.short_calls >= current_app.config['SHORT_CALL_MAX_AMOUNT']:
        return True
    return False

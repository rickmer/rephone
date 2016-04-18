from app.models import db, CallStatistics
from datetime import datetime


def log_call(call_duration, id_campaign):
    """
    log call statistics
    :param call_duration: duration on the call in seconds
    :param id_campaign: id of the campaign
    """
    call = CallStatistics(time=datetime.now(),
                          duration=int(call_duration),
                          campaign=int(id_campaign))
    db.session.add(call)
    db.session.commit()

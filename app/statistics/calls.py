from app.models import db, CallStatistics
from datetime import datetime


def log_call(duration):
    call_time = CallStatistics(time=datetime.now(),
                               typ='seconds',
                               data=int(duration))
    call_event = CallStatistics(time=datetime.now(),
                                typ='call',
                                data=1)
    db.session.add(call_time)
    db.session.add(call_event)
    db.session.commit()

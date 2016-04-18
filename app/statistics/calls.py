from app.models import db, CallStatistics, Campaign
from datetime import datetime


def log_call(call_duration, id_campaign):
    """
    log call statistics and update call minutes on campaign object
    :param call_duration: duration on the call in seconds
    :param id_campaign: id of the campaign
    """
    call = CallStatistics(time=datetime.now(),
                          duration=int(call_duration),
                          campaign=int(id_campaign))
    db.session.add(call)
    db.session.commit()

    calls = CallStatistics().query.filter_by(campaign=int(id_campaign)).all()
    seconds_already_talked = 0
    for call in calls:
        seconds_already_talked += call.duration
    campaign = Campaign().query.filter_by(id=int(id_campaign)).first()
    campaign.minutes_talked = round(seconds_already_talked / 60)
    db.session.commit()

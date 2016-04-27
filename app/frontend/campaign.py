from flask import render_template
from flask.ext.login import current_user
from app.models import Campaign, Audience


def overview():
    campaigns = Campaign().query.filter_by(id_owner=current_user.id).all()
    for campaign in campaigns:
        audience = Audience().query.filter_by(id=campaign.id_audience).first()
        campaign.id_audience = audience
    return render_template('frontend/campaign_overview.html', campaigns=campaigns)

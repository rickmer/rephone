from flask import render_template, abort, flash
from flask.ext.login import current_user
from app.models import Campaign, Audience, db
from app.forms import CampaignForm


def overview():
    """
    Render Overview of all of current users Campaigns
    :return: http response
    """
    campaigns = Campaign().query.filter_by(id_owner=current_user.id).all()
    for campaign in campaigns:
        audience = Audience().query.filter_by(id=campaign.id_audience).first()
        campaign.id_audience = audience
    return render_template('frontend/campaign_overview.html', campaigns=campaigns)


def edit(id_campaign, request):
    """
    render edit view and handle edit POST data
    :param id_campaign: id of campaign to edit
    :param request: current http request
    :return: http response
    """
    campaign = Campaign().query.filter_by(id=id_campaign).first()
    if campaign is None:
        return abort(404)
    form = CampaignForm(request.form)
    audiences = Audience().query.all()
    if request.method == 'GET':
        form.id.data = campaign.id
        form.description.data = campaign.description
        form.name.data = campaign.name
        form.target_minutes.data = campaign.target_minutes
        form.id_audience.data = campaign.id_audience
        return render_template('frontend/campaign_edit.html', form=form, audiences=audiences)
    elif request.method == 'POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            campaign.id_audience = form.id_audience.data
            campaign.name = form.name.data
            campaign.description = form.description.data
            campaign.target_minutes = form.target_minutes.data
            db.session.commit()
            flash('Saved!', category='success')
            return render_template('frontend/campaign_edit.html', form=form, audiences=audiences)
        else:
            flash('Not Saved!', category='warning')
            return render_template('frontend/campaign_edit.html', form=form, audiences=audiences)
    elif request.method == 'DELETE':
        if current_user.id == campaign.id_owner:
            db.session.delete(campaign)
            db.session.commit()
            return 'success', 200
        else:
            return abort(403)


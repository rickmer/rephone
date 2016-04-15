from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()
audience_respondent = db.Table('audience_respondent',
                               db.Column('id_audience', db.Integer(), db.ForeignKey('audience.id')),
                               db.Column('id_respondent', db.Integer(), db.ForeignKey('respondent.id')))


class Respondent(db.Model):
    """
    ORM Model for the decision makers data.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(64))
    url = db.Column(db.String(256))
    nation = db.Column(db.String(128))
    group = db.Column(db.String(128))
    party = db.Column(db.String(128))
    license = db.Column(db.String(128))
    image = db.Column(db.String(64))
    voting = db.Column(db.String(16))
    confluence = db.Column(db.String(16))


class Campaign(db.Model):
    """
    ORM model for Calling Campaigns.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    id_audience = db.Column(db.Integer)


class Audience(db.Model):
    """
    ORM model for different groups of decision makers to be addressed by a campaign.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    respondents = db.relationship('Respondent',
                                  secondary=audience_respondent,
                                  backref=db.backref('respondents', lazy='dynamic'))


class RandomBias(db.Model):
    """
    ORM model for biased random distribution.
    """
    id = db.Column(db.Integer(), primary_key=True)
    id_audience = db.Column(db.Integer())
    id_respondent = db.Column(db.Integer())
    vector_index = db.Column(db.Integer())
    distribution_value = db.Column(db.BigInteger())


class PossibleAbuses(db.Model):
    """
    ORM model for usage data to detect and prevent abuse.
    """
    id = db.Column(db.String(64), primary_key=True)
    short_calls = db.Column(db.Integer())
    date = db.Column(db.Date())
    persistent = db.Column(db.Boolean())


class BlockedClients(db.Model):
    """
    ORM model for ip addresses to block
    """
    id = db.Column(db.String(64), primary_key=True)
    calls = db.Column(db.Integer())
    date = db.Column(db.Date())
    persistent = db.Column(db.Boolean())


class CallStatistics(db.Model):
    """
    ORM model for call statistics
    """
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.DateTime())
    typ = db.Column(db.String(12))
    data = db.Column(db.Integer())

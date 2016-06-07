from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
db = SQLAlchemy()


audience_respondent = db.Table('audience_respondent',
                               db.Column('id_audience',
                                         db.Integer(),
                                         db.ForeignKey('audience.id')),
                               db.Column('id_respondent',
                                         db.Integer(),
                                         db.ForeignKey('respondent.id')))

roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('role.id')))


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


class Campaign(db.Model):
    """
    ORM model for Calling Campaigns.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    id_audience = db.Column(db.Integer)
    target_minutes = db.Column(db.Integer())
    minutes_talked = db.Column(db.Integer())
    id_owner = db.Column(db.Integer())
    campaign_text = db.Column(db.String(2048))
    campaign_text_html = db.Column(db.String(8192))


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
    campaign = db.Column(db.Integer())
    duration = db.Column(db.Integer())


class Role(db.Model, RoleMixin):
    """
    ORM model in role object
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """
    ORM model user object
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User id=%s email=%s>' % (self.id, self.email)

user_data_store = SQLAlchemyUserDatastore(db=db, role_model=Role, user_model=User)

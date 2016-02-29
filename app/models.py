from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()
audience_respondent = db.Table('audience_respondent',
                               db.Column('id_audience', db.Integer(), db.ForeignKey('audience.id')),
                               db.Column('id_respondent', db.Integer(), db.ForeignKey('respondent.id')))


class Respondent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    institution = db.Column(db.String(64))
    telefon_nr = db.Column(db.String(32))
    url = db.Column(db.String(256))
    email = db.Column(db.String(64))
    image = db.Column(db.String(64))


class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    id_audience = db.Column(db.Integer)


class Audience(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    respondents = db.relationship('Respondent',
                                  secondary=audience_respondent,
                                  backref=db.backref('respondents', lazy='dynamic'))

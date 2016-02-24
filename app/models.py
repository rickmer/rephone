from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class MitgliedDesBundestages(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    fraktion = db.Column(db.String(64))
    telefon_nr = db.Column(db.String(32))
    url = db.Column(db.String(256))
    email = db.Column(db.String(64))
    image = db.Column(db.String(64))

from flask import Flask
from .models import db


def create_app():
    from .views import main as main_blueprint
    app = Flask(__name__)
    app.config.from_object('app.config.database')
    app.config.from_object('app.config.security')
    app.config.from_object('app.config.twilio')
    db.init_app(app=app)
    app.register_blueprint(main_blueprint)
    db.create_all(app=app)
    return app

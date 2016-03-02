from flask import Flask
from .models import db


def create_app(config_override=None):
    from .views import main as main_blueprint
    app = Flask(__name__)
    app.config['demo_mode'] = False
    app.config.from_object('app.config.database')
    app.config.from_object('app.config.security')
    app.config.from_object('app.config.twilio')
    if config_override:
        for key in config_override:
            app.config[key] = config_override[key]
    db.init_app(app=app)
    app.register_blueprint(main_blueprint)
    db.create_all(app=app)
    return app

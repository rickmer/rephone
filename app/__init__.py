from flask import Flask
from .models import db
from flask.ext.captcha import Captcha


def create_app(config_override=None):
    from .views import main as main_blueprint
    from flask.ext.captcha.views import captcha_blueprint
    app = Flask(__name__)
    # parse configuration
    app.config['demo_mode'] = False
    app.config.from_object('app.config.database')
    app.config.from_object('app.config.security')
    app.config.from_object('app.config.twilio')
    app.config.from_object('app.config.captcha')
    if config_override:
        for key in config_override:
            app.config[key] = config_override[key]
    # initialize database
    db.init_app(app=app)
    # initialize captcha
    if app.config['CAPTCHA_ACTIVATED']:
        captcha = Captcha()
        captcha.init_app(app=app)
        app.register_blueprint(captcha_blueprint, url_prefix='/captcha')
    db.create_all(app=app)
    # register blueprints
    app.register_blueprint(main_blueprint)

    @app.context_processor
    def inject_into_jinja_templates():
        return dict(captcha_activated=app.config['CAPTCHA_ACTIVATED'])

    return app

from flask import Flask
from .models import db, user_data_store
from .forms import RegisterForm
from flask.ext.captcha import Captcha
from flask.ext.mail import Mail
from flask.ext.security import Security

mail = Mail()
security = Security()


def create_app(config_override=None, config_file=None):
    from .views import main as main_blueprint
    from flask.ext.captcha.views import captcha_blueprint
    app = Flask(__name__)
    # parse configuration
    app.config['demo_mode'] = False
    app.config.from_object('app.config.database')
    app.config.from_object('app.config.security')
    app.config.from_object('app.config.twilio')
    app.config.from_object('app.config.captcha')
    app.config.from_object('app.config.impressum')
    app.config.from_object('app.config.abuse')
    app.config.from_object('app.config.smtp')
    app.config.from_object('app.config.social')
    if config_override:
        for key in config_override:
            app.config[key] = config_override[key]
    if config_file:
        app.config.from_pyfile(filename='/'.join(['..', config_file]))
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

    mail.init_app(app=app)
    security.init_app(app=app, datastore=user_data_store, confirm_register_form=RegisterForm)

    @app.context_processor
    def inject_into_jinja_templates():
        return dict(captcha_activated=app.config['CAPTCHA_ACTIVATED'],
                    social_activated=app.config['SOCIAL_ACTIVATED'],
                    impressum=app.config['IMPRESSUM'])
    # initialize biased pseudo random distribution
    with app.app_context():
        from .random.bias import BiasedRandomValue
        app.random = BiasedRandomValue()

    return app

from flask import Flask


def create_app():
    from .views import main as main_blueprint
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    return app

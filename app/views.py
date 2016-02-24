from flask import Blueprint, render_template
main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    from .models import MitgliedDesBundestages
    from random import randint
    random_id = randint(1, 631)
    record = MitgliedDesBundestages().query.filter_by(id=random_id).first()
    return render_template('callform.html', record=record)

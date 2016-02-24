from flask import Blueprint, render_template
main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    from .models import MitgliedDesBundestages
    record = MitgliedDesBundestages().query.filter_by(id=1).first()
    return render_template('callform.html', record=record)

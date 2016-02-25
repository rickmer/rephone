from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class CallForm(Form):
    id_mdb = IntegerField(validators=[DataRequired()])
    phone_number = StringField(validators=[DataRequired(), Length(1, 64)])

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(CallForm, self).validate()
        if not initial_validation:
            return False
        return True

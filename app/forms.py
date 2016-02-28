from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class CallForm(Form):
    id_mdb = IntegerField(validators=[DataRequired()])
    phone_number = StringField(validators=[DataRequired(message=u'Dieses Feld ist erforderlich.'), Length(1, 64)])

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)

    def validate(self):
        from .phone_number import PhoneNumber
        initial_validation = super(CallForm, self).validate()
        if not initial_validation:
            return False
        if not PhoneNumber(self.phone_number).is_from(49):
            self.phone_number.errors.append('Dies ist keine deutsche Rufnummer.')
            return False
        return True

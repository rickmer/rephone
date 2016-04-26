from flask import current_app
from flask.ext.captcha.models import CaptchaStore
from flask.ext.wtf import Form
from flask_security import ConfirmRegisterForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class CallForm(Form):
    """
    WTForm to validate Phonenumber and csrf-token
    """
    id_mdb = IntegerField(validators=[DataRequired()])
    phone_number = StringField(validators=[DataRequired(message=u'Dieses Feld ist erforderlich.'), Length(1, 64)])
    captcha = StringField()
    captcha_hash = StringField()

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)

    def validate(self):
        from app.callwidget.phone_number import PhoneNumber
        initial_validation = super(CallForm, self).validate()
        if not initial_validation:
            return False
        if current_app.config['CAPTCHA_ACTIVATED'] and \
           not CaptchaStore.validate(hashkey=self.captcha_hash.data,
                                     response=str(self.captcha.data).strip().lower()):
            self.captcha.errors.append('Bitte versuchen sie es erneut.')
            return False
        if not PhoneNumber(self.phone_number).is_from(49):
            self.phone_number.errors.append('Dies ist keine deutsche Rufnummer.')
            return False

        self.phone_number.data = PhoneNumber(self.phone_number).get_e164_format()
        return True


class RegisterForm(ConfirmRegisterForm):
    username = StringField('Username', validators=[DataRequired()])
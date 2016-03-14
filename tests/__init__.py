from flask.ext.testing import TestCase
from app import create_app


class RephoneTest(TestCase):

    def create_app(self):
        config = {'WTF_CSRF_ENABLED': False,
                  'CAPTCHA_ACTIVATED': False}
        test_app = create_app(config_override=config)
        return test_app

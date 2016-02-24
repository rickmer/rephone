from flask.ext.testing import TestCase
from app import create_app


class RephoneTest(TestCase):

    def create_app(self):
        test_app = create_app()
        return test_app

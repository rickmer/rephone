from re import sub
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class PhoneNumber(object):

    def __init__(self, nr):
        self.phone_number = sub(r'\s', '', str(nr))
        self.phone_number = sub(r'/', '', self.phone_number)
        self.phone_number = sub(r'\-', '', self.phone_number)
        self.phone_number = sub(r'\(', '', self.phone_number)
        self.phone_number = sub(r'\)', '', self.phone_number)
        self.phone_number = sub(r'\\', '', self.phone_number)
        try:
            self.phone_number = phonenumbers.parse(self.phone_number, None)
        except NumberParseException:
            self.phone_number = phonenumbers.parse(self.phone_number, 'DE')
        finally:
            return None
        return self.phone_number

    def is_from(self, country_code):
        return self.phone_number.country_code == country_code

    def get_e164_format(self):
        return ''.join(['+', str(self.phone_number.country_code), str(self.phone_number.national_number)])
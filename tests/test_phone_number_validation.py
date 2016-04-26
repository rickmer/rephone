from app.callwidget.phone_number import PhoneNumber


def test_ill_number_1():
    assert PhoneNumber('+00490301234567').get_e164_format() == '+49301234567'


def test_ill_number_2():
    assert PhoneNumber('(00)49(0)301234567').get_e164_format() == '+49301234567'


def test_ill_number_3():
    assert PhoneNumber('030/1234567').get_e164_format() == '+49301234567'


def test_ill_number_4():
    assert PhoneNumber('030-1234567').get_e164_format() == '+49301234567'


def test_ill_number_5():
    assert PhoneNumber('(+4930)1234567').get_e164_format() == '+49301234567'


def test_ill_number_6():
    assert PhoneNumber('+0049301234567').get_e164_format() == '+49301234567'


def test_ill_number_7():
    assert PhoneNumber('0160123456789').get_e164_format() == '+49160123456789'


def test_ill_number_8():
    assert PhoneNumber('+490160123456789').get_e164_format() == '+49160123456789'


def test_ill_number_9():
    assert PhoneNumber('0160\\123456789').get_e164_format() == '+49160123456789'


def test_ill_number_10():
    assert PhoneNumber('00490160123456789').get_e164_format() == '+49160123456789'

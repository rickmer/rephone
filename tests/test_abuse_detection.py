from . import RephoneTest
from re import match


class TestAbuseDetection(RephoneTest):

    def test_add_short_call(self):
        with self.client:
            for _ in range(0, 10):
                self.client.post('/outbound/status/',
                                 data=dict(To='+49301234567890',
                                           CallDuration=39))
            response = self.client.post('/', data=dict(id_mdb=1,
                                                       phone_number='+49301234567890'))
            assert match(r'.*sorry Dave.*', str(response.get_data()))
from . import RephoneTest
from re import match


class CallCounterTest(RephoneTest):

    def test_counter(self):
        with self.client:
            self.client.post('outbound/status/2',
                             data=dict(To='+49401234567890',
                                       CallDuration=600))
            response = self.client.get('/2')
            print(response.get_data())
            assert match(r'.*width: 3.3333333333333335%.*', str(response.get_data()))

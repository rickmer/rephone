from . import RephoneTest
from re import match


class TestViews(RephoneTest):

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            assert response.status_code == 200

    def test_outbound(self):
        with self.client:
            response = self.client.post('/outbound/1')
            assert response.status_code == 200
            assert match(r'.*<Dial><Number>\+32022845572</Number></Dial>.*', str(response.get_data()))

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
            assert match(r'.*<Dial><Number>\+493022772600</Number></Dial>.*', str(response.get_data()))

    def test_phone_number_validation(self):
        with self.client:
            response = self.client.post('/', data=dict(id_mdb='1', phone_number='+45123456789'))
            assert response.status_code == 200
            assert match(r'.*Dies ist keine deutsche Rufnummer.*', str(response.get_data()))
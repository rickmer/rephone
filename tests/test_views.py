from . import RephoneTest


class TestViews(RephoneTest):

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            assert response.status_code == 200

    def test_outbound(self):
        from re import match
        with self.client:
            response = self.client.post('/outbound/1')
            assert response.status_code == 200
            assert match(r'.*<Dial><Number>\+493022772600</Number></Dial>.*', str(response.get_data()))

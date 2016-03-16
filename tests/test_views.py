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

    def test_bias_alteration(self):
        index_0_before = self.app.random[0][0]
        index_1_before = self.app.random[0][1]
        self.app.random.add_sample(audience_id=1, respondent_id=1)
        index_0_after = self.app.random[0][0]
        index_1_after = self.app.random[0][1]

        assert index_0_before == index_0_after
        assert index_1_before == index_1_after - 1

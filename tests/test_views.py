from . import RephoneTest
from re import match


class TestViews(RephoneTest):

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            assert response.status_code == 303

    def test_outbound(self):
        with self.client:
            response = self.client.post('/outbound/1')
            assert response.status_code == 200
            assert match(r'.*<Dial><Number>\+33388175572</Number></Dial>.*', str(response.get_data()))

    def test_outbound_test_number(self):
        with self.client:
            self.app.config['TWILIO_TEST_NUMBER'] = '+4940123456789'
            response = self.client.post('/outbound/1')
            assert response.status_code == 200
            assert match(r'.*<Dial><Number>\+4940123456789</Number></Dial>.*', str(response.get_data()))

    def test_bias_alteration_audience_1(self):
        index_0_before = self.app.random[1][0]
        index_1_before = self.app.random[1][1]
        self.app.random.add_sample(audience_id=1, respondent_id=1)
        index_0_after = self.app.random[1][0]
        index_1_after = self.app.random[1][1]

        assert index_0_before == index_0_after
        assert index_1_before == index_1_after - 1

    def test_bias_alteration_audience_2(self):
        index_0_before = self.app.random[2][0]
        index_1_before = self.app.random[2][1]
        self.app.random.add_sample(audience_id=2, respondent_id=752)
        index_0_after = self.app.random[2][0]
        index_1_after = self.app.random[2][1]

        assert index_0_before == index_0_after
        assert index_1_before == index_1_after - 1

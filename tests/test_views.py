from . import RephoneTest


class TestViews(RephoneTest):

    def test_index(self):
        with self.client:
            response = self.client.get('/')
            assert response.status_code == 200

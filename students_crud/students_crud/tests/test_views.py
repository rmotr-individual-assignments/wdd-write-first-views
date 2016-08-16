from django.test import TestCase


class StatusViewTestCase(TestCase):

    def test_status_view(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'OK'})

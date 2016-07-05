import json

from rest_framework.test import APITestCase


class PandStatusTest(APITestCase):

    def test_simple_response(self):
        """
        Verify that the endpoint exists.
        """
        response = self.client.get('/zwaailicht/pand_status/0363010003761571/')
        self.assertEquals(200, response.status_code)

    def test_response_contains_locatie_met_bag_id(self):
        response = self.client.get('/zwaailicht/pand_status/0363010003761571/')
        self.assertIn('locatie', response.data)
        self.assertIn('bag_id', response.data['locatie'])
        self.assertEqual('0363010003761571', response.data['locatie']['bag_id'])

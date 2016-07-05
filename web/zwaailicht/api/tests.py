import json

from rest_framework.test import APITestCase


class PandStatusTest(APITestCase):

    def test_simple_response(self):
        """
        Verify that the endpoint exists.
        """
        response = self.client.get('/zwaailicht/status_pand/0363010000758545/')
        self.assertEquals(200, response.status_code)

    def test_response_contains_locatie_met_bag_id(self):
        response = self.client.get('/zwaailicht/status_pand/0363010000758545/')
        self.assertIn('locatie', response.data)
        self.assertIn('bag_id', response.data['locatie'])
        self.assertEqual('0363010000758545', response.data['locatie']['bag_id'])

    def test_response_contains_indicatoren(self):
        response = self.client.get('/zwaailicht/status_pand/0363010000758545/')
        self.assertIn('indicatoren', response.data)

        indicatoren = response.data['indicatoren']
        self.assertTrue(len(indicatoren) >= 1)

        self.assertEqual('Status pand', indicatoren[0]['indicator'])
        self.assertEqual(1, indicatoren[0]['waarschuwingsniveau'])
        self.assertEqual('Beperking pand', indicatoren[0]['label'])
        self.assertEqual('Splitsing pand zonder vergunning [Status]', indicatoren[0]['aanvullende_informatie'])


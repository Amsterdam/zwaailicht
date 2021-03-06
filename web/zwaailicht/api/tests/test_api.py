from django.test import override_settings
from rest_framework.test import APITestCase

from api.tests.fixtures import patch_requests


@patch_requests
@override_settings(
    VBO_URI_TEMPLATE="http://api/bag/verblijfsobject/{landelijk_id}/",
    MAPPING_FILE='api/tests/fixture_files/mapping.json'
)
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
        self.assertEqual(3, indicatoren[0]['waarschuwingsniveau'])
        self.assertEqual('Beperking pand', indicatoren[0]['label'])
        self.assertEqual('Splitsing pand zonder vergunning [Status]',
                         indicatoren[0]['aanvullende_informatie'])

    def test_unknown_vbo_is_404(self):
        response = self.client.get('/zwaailicht/status_pand/1234/')
        self.assertEquals(404, response.status_code)

    def test_known_vbo_unknown_follow_is_200(self):
        response = self.client.get('/zwaailicht/status_pand/0363010001958552/')
        self.assertEquals(200, response.status_code)


@patch_requests
@override_settings(
    VBO_URI_TEMPLATE="http://api/bag/verblijfsobject/{landelijk_id}/",
    MAPPING_FILE='api/tests/fixture_files/mapping.json'
)
class GebruikTest(APITestCase):
    def test_simple_response(self):
        """
        Verify that the endpoint exists
        :return:
        """
        response = self.client.get('/zwaailicht/gebruik/0363010000758545/')
        self.assertEquals(200, response.status_code)

    def test_response_contains_locatie_met_bag_id(self):
        response = self.client.get('/zwaailicht/gebruik/0363010000758545/')
        self.assertIn('locatie', response.data)
        self.assertIn('bag_id', response.data['locatie'])
        self.assertEqual('0363010000758545', response.data['locatie']['bag_id'])

    def test_response_contains_indicatoren(self):
        response = self.client.get('/zwaailicht/gebruik/0363010000758545/')
        self.assertIn('indicatoren', response.data)

        indicatoren = response.data['indicatoren']
        self.assertTrue(len(indicatoren) >= 1)

        self.assertEqual('Gebruik', indicatoren[0]['indicator'])
        self.assertEqual(3, indicatoren[0]['waarschuwingsniveau'])
        self.assertEqual('Info gebruik', indicatoren[0]['label'])
        self.assertEqual('cultuur', indicatoren[0]['aanvullende_informatie'])

    def test_unknown_vbo_is_404(self):
        response = self.client.get('/zwaailicht/gebruik/1234/')
        self.assertEquals(404, response.status_code)

    def test_None_fields_is_200(self):
        response = self.client.get('/zwaailicht/gebruik/0363010000686941/')
        self.assertEquals(200, response.status_code)


@patch_requests
@override_settings(
    VBO_URI_TEMPLATE="http://api/bag/verblijfsobject/{landelijk_id}/",
    MAPPING_FILE='api/tests/fixture_files/mapping.json'
)
class BouwlagenTest(APITestCase):
    def test_simple_response(self):
        """
        Verify that the endpoint exists
        """
        response = self.client.get('/zwaailicht/bouwlagen/0363010000758545/')
        self.assertEquals(200, response.status_code)

    def test_response_contains_locatie_met_bag_id(self):
        response = self.client.get('/zwaailicht/bouwlagen/0363010000758545/')
        self.assertIn('locatie', response.data)
        self.assertIn('bag_id', response.data['locatie'])
        self.assertEqual('0363010000758545', response.data['locatie']['bag_id'])

    def test_response_with_null_contains_indicatoren(self):
        response = self.client.get('/zwaailicht/bouwlagen/0363010000758545/')
        self.assertIn('indicatoren', response.data)

        indicatoren = response.data['indicatoren']
        self.assertListEqual([], indicatoren)

    def test_response_meerdere_verdiepingen(self):
        response = self.client.get('/zwaailicht/bouwlagen/0363010012099785/')
        self.assertIn('indicatoren', response.data)

        indicatoren = response.data['indicatoren']
        self.assertNotEqual([], indicatoren)

        self.assertDictEqual({
            'waarschuwingsniveau': 2,
            'indicator': 'Bouwlagen pand',
            'label': 'Hoog gebouw',
            'aanvullende_informatie': 'Aantal bouwlagen: 13',
        }, indicatoren[0])

    def test_response_ingang(self):
        response = self.client.get('/zwaailicht/bouwlagen/0363010000783909/')
        self.assertIn('indicatoren', response.data)

        indicatoren = response.data['indicatoren']
        self.assertNotEqual([], indicatoren)

        self.assertDictEqual({
            'waarschuwingsniveau': 3,
            'indicator': 'Bouwlagen pand',
            'label': 'Hoog gebouw',
            'aanvullende_informatie': 'Aantal bouwlagen: 4',
        }, indicatoren[0])

        self.assertDictEqual({
            "waarschuwingsniveau": 3,
            "indicator": "Bouwlagen pand",
            "aanvullende_informatie": "Toegang op verdieping 1",
            "label": "Toegang op verdieping"
        }, indicatoren[1])

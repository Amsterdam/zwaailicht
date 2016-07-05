from rest_framework.test import APITestCase


class PandStatusTest(APITestCase):

    def test_simple_response(self):
        """
        Verify that the endpoint exists.
        """
        response = self.client.get('/zwaailicht/pand_status/0363010003761571/')
        self.assertEquals(200, response.status_code)

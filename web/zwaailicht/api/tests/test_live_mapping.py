from django.test import TestCase

from api import mapping


class LiveMappingTest(TestCase):
    """
    Tests on the mapping.json that is used by the application, as opposed to tests on the mapping.json
    in the fixture_files directory.

    Used to validate consistency of the file.
    """

    def setUp(self):
        self.mapping = mapping.Mapping()

    def assertContainsValues(self, results):
        filtered = [r for r in results if r is not None]
        self.assertNotEqual([], filtered)

    def test_mapping_aantal_bouwlagen(self):
        results = [self.mapping.map_aantal_bouwlagen(i) for i in range(0, 15)]
        self.assertContainsValues(results)

    def test_mapping_verdieping_toegang(self):
        results = [self.mapping.map_verdieping_toegang(i) for i in
                   range(-20, 20)]
        self.assertContainsValues(results)

    def test_mapping_pand_status(self):
        results = [self.mapping.map_pand_status(str(i)) for i in range(10, 99)]
        self.assertContainsValues(results)

    def test_gebruikscode(self):
        results = [self.mapping.map_gebruikscode(str(i)) for i in
                   range(1000, 4000)]
        self.assertContainsValues(results)

    def test_gebruiksdoel(self):
        results = [self.mapping.map_gebruiksdoel(str(i)) for i in
                   range(1000, 4000)]
        self.assertContainsValues(results)

    def test_mapping_beperking(self):
        codes = ['KW', 'HV', 'OH', 'WV',
                 'WG']  # a bit more brittle than the others, sorry
        results = [self.mapping.map_beperking(c) for c in codes]
        self.assertContainsValues(results)

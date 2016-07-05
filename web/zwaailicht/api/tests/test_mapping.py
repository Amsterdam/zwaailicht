from unittest import TestCase

from .. import mapping


class MappingTest(TestCase):

    def setUp(self):
        self.mapping = mapping.Mapping()

    def test_beperking_GG_status_pand(self):
        indicator = self.mapping.beperking_to_status_pand('GG')
        self.assertDictEqual({
            'indicator': 'Status pand',
            'waarschuwingsniveau': 2,
            'label': 'Beperking pand',
            'aanvullende_informatie': 'Monument [Status]',
        }, indicator)

    def test_beperking_GU_status_pand(self):
        indicator = self.mapping.beperking_to_status_pand('GU')
        self.assertIsNone(indicator)

    def test_beperking_niet_bestaand_status_pand(self):
        indicator = self.mapping.beperking_to_status_pand('DIT_IS_GEEN_CODE')
        self.assertIsNone(indicator)



from django.test import TestCase

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

    def test_pand_status_24_status_pand(self):
        indicator = self.mapping.pand_status_to_status_pand('24')
        self.assertDictEqual({
            'indicator': 'Status pand',
            'waarschuwingsniveau': 2,
            'label': 'Pand in bouwfase',
            'aanvullende_informatie': 'Pand in bouwfase [Status]',
        }, indicator)

    def test_pand_status_number_24_status_pand(self):
        indicator_str = self.mapping.pand_status_to_status_pand('24')
        indicator_int = self.mapping.pand_status_to_status_pand(24)
        self.assertDictEqual(indicator_str, indicator_int)

    def test_pand_status_31(self):
        self.assertIsNone(self.mapping.pand_status_to_status_pand(31))

    def test_pand_status_unknown(self):
        self.assertIsNone(self.mapping.pand_status_to_status_pand("IK_BEN_OOK_GEEN_CODE"))

    def test_gebruikscode_3333(self):
        indicator = self.mapping.gebruikscode_to_gebruik('3333')
        self.assertDictEqual({
            'indicator': 'Gebruik',
            "label": "Kwetsbare doelgroep",
            "aanvullende_informatie": "medisch dagverblijf",
            "waarschuwingsniveau": 2
        }, indicator)

    def test_gebruiksdoel_1043(self):
        indicator = self.mapping.gebruiksdoel_to_gebruik('1043')
        self.assertDictEqual({
            "indicator": "Gebruik",
            "label": "Woning met invalide(n)",
            "aanvullende_informatie": "Invalideeenheid",
            "waarschuwingsniveau": 2
        }, indicator)




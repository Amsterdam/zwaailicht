import csv
import json


class Mapping(object):
    """
    Mapping from WKPB and BAG+ attributes to Indicatoren.
    """

    def __init__(self):
        with open('mapping.json') as f:
            self.mapping = json.load(f)

    def _get_indicator(self, indicator, field, value):
        result = self.mapping[indicator][field].get(str(value))

        if not result:
            return None
        if not result.get('waarschuwingsniveau'):
            return None
        return result

    def beperking_to_status_pand(self, beperking_code):
        return self._get_indicator('Status pand', 'Beperking.beperkingcode', beperking_code)

    def pand_status_to_status_pand(self, pand_status):
        return self._get_indicator('Status pand', 'Pand.Pandstatus', pand_status)

    def json(self):
        return self.mapping

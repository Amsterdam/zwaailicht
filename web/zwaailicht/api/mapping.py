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

        if result and not result.get('waarschuwingsniveau'):
            return None

        return result

    def map_beperking(self, beperking_code):
        """
        Return the indicator associated with WKPB Beperking code, if any.
        """
        return self._get_indicator('Status pand', 'Beperking.beperkingcode', beperking_code)

    def map_pand_status(self, pand_status):
        """
        Return the indicator associated with BAG Pand status code, if any.
        """
        return self._get_indicator('Status pand', 'Pand.Pandstatus', pand_status)

    def map_gebruikscode(self, gebruikscode):
        """
        Return the indicator associated with BAG Verblijfsobject gebruikscode, if any.
        """
        return self._get_indicator('Gebruik', 'Verblijfsobject.gebruikscode', gebruikscode)

    def map_gebruiksdoel(self, gebruiksdoel):
        """
        Return the indicator associated with BAG-plus Verblijfsobject gebruiksdoel, if any.
        """
        return self._get_indicator('Gebruik', 'Verblijfsobject.gebruiksdoel-plus', gebruiksdoel)

    def json(self):
        return self.mapping

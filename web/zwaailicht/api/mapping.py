import json

from django.conf import settings

_LARGE = 1000000


def _is_in_range(value, range_definition):
    range_parts = range_definition.split('..')
    if len(range_parts) != 2:
        raise ValueError("Incorrect range definition: {}".format(range_definition))

    lower, upper = range_parts
    lower = int(lower) if lower else -_LARGE
    upper = int(upper) if upper else _LARGE

    return lower <= value <= upper


def get_from_table_by_range(table, request):
    if request is None:
        return None

    results = [v for (range_definition, v) in table.items() if _is_in_range(request, range_definition)]

    if not results:
        return None

    if len(results) == 1:
        return results[0]

    raise ValueError("Overlapping ranges found for value {}".format(request))


class Mapping(object):
    """
    Mapping from WKPB and BAG+ attributes to Indicatoren.
    """

    def __init__(self):
        with open(settings.MAPPING_FILE) as f:
            self.mapping = json.load(f)

    def _update_result(self, result, requested_value):
        if not result:
            return None

        if result.get('waarschuwingsniveau') == 4:
            return None

        result['aanvullende_informatie'] = result['aanvullende_informatie'].format(waarde=requested_value)
        return result

    def _get_indicator(self, indicator, field, value):
        table = self.mapping[indicator][field]
        result = table.get(str(value))

        return self._update_result(result, value)

    def _get_indicator_by_range(self, indicator, field, value):
        table = self.mapping[indicator][field]
        result = get_from_table_by_range(table, value)

        return self._update_result(result, value)

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

    def map_verdieping_toegang(self, verdieping_toegang):
        """
        Return the indicator associated with BAG Verblijfsobject verdieping toegang, if any.
        """
        return self._get_indicator_by_range('Bouwlagen pand', 'Verblijfsobject.Verdieping toegang', verdieping_toegang)

    def map_aantal_bouwlagen(self, aantal_bouwlagen):
        """
        Return the indicator associated with BAG Verblijfsobject aantal bouwlagen. if any.
        """
        return self._get_indicator_by_range('Bouwlagen pand', 'Verblijfsobject.Aantal bouwlagen', aantal_bouwlagen)

    def json(self):
        return self.mapping

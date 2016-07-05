import csv
import json


class Mapping(object):
    """
    Mapping from WKPB and BAG+ attributes to Indicatoren.
    """

    def __init__(self):
        with open('mapping.json') as f:
            self.mapping = json.load(f)

    def beperking_to_status_pand(self, beperking_code):
        result = self.mapping['Status pand']['Beperking.beperkingcode'].get(beperking_code)
        if not result:
            return None

        if not result.get('waarschuwingsniveau'):
            return None

        return result

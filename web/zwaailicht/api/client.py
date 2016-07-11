import logging

import requests
from django.conf import settings

log = logging.getLogger(__name__)


class Verblijfsobject(object):
    """
    Wrapper object for VBO JSON
    """

    def __init__(self, json):
        self._json = json
        self.landelijk_id = json.get('verblijfsobjectidentificatie')
        self.panden = json.get('panden', {}).get('href')
        self.beperkingen = json.get('beperkingen', {}).get('href')

    def __str__(self):
        return "VBO({})".format(self.landelijk_id)


class Pand(object):
    """
    Wrapper object for Pand JSON
    """

    def __init__(self, json):
        self._json = json
        self.pand_status = json.get('status', {}).get('code')


class Beperking(object):
    """
    Wrapper object for WKPB Beperking JSON
    """

    def __init__(self, json):
        self._json = json
        self.beperking = json.get('beperkingcode', {}).get('code')


class Client(object):
    """
    Client for obtaining data from the BAG.
    """

    def __init__(self):
        pass

    def get_vbo(self, landelijk_id):
        """
        Obtains a verblijfsobject.

        :param landelijk_id: string
        """
        assert landelijk_id is not None

        url = settings.VBO_URI_TEMPLATE.format(landelijk_id=landelijk_id)

        res = requests.get(url)
        if not res.ok:
            log.warn("Could not retrieve VBO %s from %s", landelijk_id, url)
            return None

        return Verblijfsobject(res.json())

    def get_panden(self, vbo):
        """
        Returns all Pand objects related to a Verblijfsobject
        :param vbo:
        :return: a list of Pand objects, never None
        """
        url = vbo.panden

        res = requests.get(url)
        if not res.ok:
            log.warn("Could not retrieve panden for VBO %s from %s", vbo, url)
            return []

        pand_urls = [obj.get('_links', {}).get('self', {}).get('href') for obj in res.json().get('results', [])]
        pand_responses = [requests.get(u) for u in pand_urls]

        return [Pand(res.json()) for res in pand_responses if res.ok]

    def get_beperkingen(self, vbo):
        """
        Returns all Beperking objects related to a Verblijfsobject
        :param vbo:
        :return: a list of Beperking objects, never None
        """
        url = vbo.beperkingen

        res = requests.get(url)
        if not res.ok:
            log.warn("Could not retrieve beperkingen for VBO %s from %s", vbo, url)
            return []

        beperking_urls = [obj.get('_links', {}).get('self', {}).get('href') for obj in res.json().get('results', [])]
        beperking_responses = [requests.get(u) for u in beperking_urls]

        return [Beperking(res.json()) for res in beperking_responses if res.ok]

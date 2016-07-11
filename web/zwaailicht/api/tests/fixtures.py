import os
from unittest import mock

import requests

fixture_mappings = {
    'http://api/bag/verblijfsobject/0363010000998532/': 'verblijfsobject/0363010000998532.json',
    'http://api/bag/verblijfsobject/0363010000758545/': 'verblijfsobject/0363010000758545.json',
    'http://api/bag/verblijfsobject/0363010001958552/': 'verblijfsobject/0363010001958552.json',
    'http://api/bag/verblijfsobject/0363010000686941/': 'verblijfsobject/0363010000686941.json',
    'http://api/bag/pand/03630012964017/': 'pand/03630012964017.json',
    'http://api/bag/pand/03630013059145/': 'pand/03630013059145.json',
    'http://api/wkpb/beperking/3488/': 'beperking/3488.json',

    'http://api/wkpb/beperking/?verblijfsobjecten__id=03630000758545':
        'beperking/verblijfsobjecten_0363010000758545.json',
    'http://api/bag/pand/?verblijfsobjecten__id=03630000998532':
        'pand/verblijfsobjecten_0363010000998532.json',
    'http://api/bag/pand/?verblijfsobjecten__id=03630000758545':
        'pand/verblijfsobjecten_0363010000758545.json',
}
directory = os.path.dirname(__file__)


def _fixtures_get(url, *args, **kwargs):
    res = requests.Response()
    res.encoding = "UTF-8"

    if url not in fixture_mappings:
        res.status_code = 404
    else:
        res.status_code = 200

        with open('{}/fixture_files/{}'.format(directory, fixture_mappings[url]), 'rb') as f:
            res._content = f.read()

    return res


def patch_requests(f):
    """
    Decorator to patch the `requests` API to return files from the fixture_files directory.
    """
    return mock.patch('requests.get', _fixtures_get)(f)

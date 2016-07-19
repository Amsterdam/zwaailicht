import os
from unittest import mock

import requests

directory = os.path.dirname(__file__)


def _fixtures_get(url, *args, **kwargs):
    filename = url
    if filename.endswith('/'):
        filename = filename[:-1]

    filename += '.json'

    filename = filename.replace('http://api/', '').replace('?', '')

    res = requests.Response()
    res.encoding = "UTF-8"

    try:
        with open('{}/fixture_files/{}'.format(directory, filename), 'rb') as f:
            res._content = f.read()
            res.status_code = 200
    except FileNotFoundError:
        res.status_code = 400

    return res


def patch_requests(f):
    """
    Decorator to patch the `requests` API to return files from the fixture_files directory.
    """
    return mock.patch('requests.get', _fixtures_get)(f)

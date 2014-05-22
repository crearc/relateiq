import datetime
import requests
import simplejson
import xml.etree.ElementTree as ET
import re
import os

import relateiq

API_HOST = 'api.relateiq.com/v2'

DATETIME_HANDLER = lambda obj: obj.isoformat() if isinstance(
    obj, datetime.datetime) else None


class Client(object):

    def __init__(self, api_key, secret_key, host=API_HOST):
        self.api_key = api_key
        self.secret_key = secret_key
        self.host = host
        
        self.session = requests.session()
        self.session.auth = (self.api_key, self.secret_key)
        self.session.headers.update({
            'User-Agent': 'relateiq-python/%s' % relateiq.get_version(),
        })

    def request(self, target, method='GET', data={}, files={}):
        assert method in ['GET', 'POST'], method

        uri = self._build_uri(target)

        if method == 'POST':
            headers = {'Content-Type': "application/json"}
            json_data = simplejson.dumps(data, default=DATETIME_HANDLER)
            response = self.session.post(uri, data=json_data,
                                         files=files, headers=headers)
        else:
            response = self.session.get(uri)

        if response.status_code == 200:
            if response.text:
                return simplejson.loads(response.text)
            else:
                return ''

        return response.text

    def _build_uri(self, target):
        proto = "https://"
        uri = "%s%s%s" % (proto, self.host, target)
        return uri

    def get_accounts(self):
        resp = self.request('/accounts')
        print resp

    def get_lists(self):
        resp = self.request('/lists')
        print resp

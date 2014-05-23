import datetime
import requests
import simplejson
import xml.etree.ElementTree as ET
import re
import string
import os

import relateiq

API_HOST = 'api.relateiq.com/v2'

DATETIME_HANDLER = lambda obj: obj.isoformat() if isinstance(
    obj, datetime.datetime) else None


RESPONSE = {
    200: "OK",
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not found",
    422: "Unprocessable entity",
    429: "Rate limit exceeded",
    500: "Internal server error",
    503: "Service unavailable; try again later"
}


class Client(object):

    def __init__(self, api_key, secret_key, host=API_HOST):
        self.api_key = api_key
        self.secret_key = secret_key
        self.host = host

        self.session = requests.session()
        self.session.auth = (self.api_key, self.secret_key)
        self.session.headers.update({
            'User-Agent': 'relateiq-python/%s' % relateiq.get_version(),
            'Accept': 'application/json'
        })

    def request(self, target, method='GET', data={}, files={}):
        assert method in ['GET', 'POST', 'PUT'], method

        uri = self._build_uri(target)

        if method == 'POST' or method == 'PUT':
            headers = {'Content-Type': "application/json"}
            json_data = simplejson.dumps(data, default=DATETIME_HANDLER)
            response = self.session.post(uri, data=json_data,
                                         files=files, headers=headers)
        else:
            response = self.session.get(uri)

        if response.status_code == 200:
            if response.text:
                return simplejson.loads(response.text)
            return ''

        print(response.text)
        raise RESPONSE[response.status_code]

    def _build_uri(self, target):
        proto = "https://"
        uri = "%s%s%s" % (proto, self.host, target)
        return uri

    def organizations(self):
        raise NotImplementedError

    def contacts(self, ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/contacts?' + query

        return self.request(uri)

    def create_contact(self, new_contact):
        method = 'POST'
        uri = '/contacts'
        return self.request(uri, method=method, data=new_contact)

    def get_contact(self, contact_id):
        uri = '/contacts/{}'.format(contact_id)
        return self.request(uri)

    def update_contact(self, contact_id, updated_contact):
        method = 'PUT'
        uri = '/contacts/{}'.format(contact_id)
        self.request(uri, method=method, data=updated_contact)

    def accounts(self, ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/accounts?' + query

        return self.request(uri)

    def create_account(self, new_account):
        uri = '/accounts'
        method = 'POST'
        data = {'name': new_account}
        return self.request(uri, method=method, data=data}

    def get_account(self, account_id):
        uri = '/accounts/{}'.format(account_id)
        return self.request(uri)

    def update_account(self, account_id, updated_account):
        uri = '/accounts/{}'.format(account_id)
        method = 'PUT'
        self.request(uri, method=method, data=updated_account)

    def lists(self, ids=None, start=0, limit=20):
        raise NotImplementedError

    def get_list(self, list_id):
        raise NotImplementedError

    def list_items(self, list_id, item_ids=None, start=0, limit=20):
        raise NotImplementedError

    def create_list_item(self, list_id, new_list_item):
        raise NotImplementedError

    def get_list_item(self, list_id, item_id):
        raise NotImplementedError

    def update_list_item(self, list_id, item_id, updated_item):
        raise NotImplementedError

    def delete_list_item(self, list_id, item_id):
        raise NotImplementedError

    def events(self):
        raise NotImplementedError

    def create_event(self, new_event):
        raise NotImplementedError

    def users(self):
        raise NotImplementedError

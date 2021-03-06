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

    def request(self, target, method, data={}, files={}):

        uri = self._build_uri(target)

        if method == 'POST' or method == 'PUT':
            headers = {'Content-Type': "application/json"}
            json_data = simplejson.dumps(data, default=DATETIME_HANDLER)
            response = self.session.post(uri, data=json_data,
                                         files=files, headers=headers)
        else:
            response = self.session.get(uri)

        if response.status_code == requests.codes.OK:
            if response.text:
                return simplejson.loads(response.text)
            return ''

        raise response.status_code, response.text

    def _build_uri(self, target):
        proto = "https://"
        uri = "%s%s%s" % (proto, self.host, target)
        return uri

    def organizations(self):
        raise NotImplementedError

    ############
    # CONTACTS #
    ############

    def contacts(self, ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/contacts?' + query
        return self.request(uri, 'GET')

    def create_contact(self, new_contact):
        return self.request('/contacts', 'POST', data=new_contact)

    def get_contact(self, contact_id):
        uri = '/contacts/{}'.format(contact_id)
        return self.request(uri, 'GET')

    def update_contact(self, contact_id, updated_contact):
        uri = '/contacts/{}'.format(contact_id)
        self.request(uri, 'PUT', data=updated_contact)

    ############
    # ACCOUNTS #
    ############

    def accounts(self, ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/accounts?' + query
        return self.request(uri, 'GET')

    def create_account(self, new_account):
        data = {'name': new_account}
        return self.request('/accounts', 'POST', data=data}

    def get_account(self, account_id):
        uri = '/accounts/{}'.format(account_id)
        return self.request(uri, 'GET')

    def update_account(self, account_id, updated_account):
        uri = '/accounts/{}'.format(account_id)
        self.request(uri, 'PUT', data=updated_account)

    #########
    # LISTS #
    #########

    def lists(self, ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/lists?' + query
        return self.request(uri, 'GET')

    def get_list(self, list_id):
        uri = '/lists/{}'.format(list_id)
        return self.request(uri, 'GET')

    ##############
    # LIST ITEMS #
    ##############

    def list_items(self, list_id, item_ids=None, start=0, limit=20):
        assert limit <= 50

        query = "_start={_start}&_limit={_limit}".format(**{
            '_start': start,
            '_limit': limit})

        if ids is not None:
            id_list = string.join(ids, ',')
            query = "_ids={}&".format(id_list) + query

        uri = '/lists/{}/listitems?'.format(list_id) + query
        return self.request(uri, 'GET')

    def create_list_item(self, list_id, new_list_item):
        uri = '/lists/{listId}/listitems'.format(
            listId=list_id)
        return self.request(uri, 'POST', data=new_list_item)

    def get_list_item(self, list_id, item_id):
        uri = '/lists/{listId}/listitems/{itemId}'.format(
            listId=list_id, itemId=item_id)
        return self.request(uri, 'GET')

    def update_list_item(self, list_id, item_id, updated_item):
        uri = '/lists/{listId}/listitems/{itemId}'.format(
            listId=list_id, itemId=item_id)
        return self.request(uri, 'PUT', data=updated_item)

    def delete_list_item(self, list_id, item_id):
        uri = '/lists/{listId}/listitems/{itemId}'.format(
            listId=list_id, itemId=item_id)
        return self.request(uri, 'DELETE')

    ##########
    # EVENTS #
    ##########

    def events(self):
        raise NotImplementedError

    def create_event(self, new_event):
        self.request('/events', 'PUT', data=new_event)

    #########
    # USERS #
    #########

    def users(self):
        raise NotImplementedError

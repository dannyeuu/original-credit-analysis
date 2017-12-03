#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

URL = 'https://sb-autenticacao-api.original.com.br/OriginalConnect'
SCOPES = 'account,investment,cars'
CALLBACK_URL = 'http://localhost:5000/integrations/original/callback'

class OriginalIntegration(object):
    """docstring for OriginalIntegration"""
    provider_name = None
    user_id = None
    headers = {'content-type': 'application/json',}
    cards = []
    invoices = []

    def __init__(self, user_id, access_token, developer_key):
        super(OriginalIntegration, self).__init__()
        self.user_id = user_id
        self.headers['developer_key'] = developer_key

        if access_token is None:
            self.get_auth()
        
        self.headers['access_token'] = access_token

    def import_original_invoices(user_id):
        pass

    # Import Cards
    def import_original_cards(self):
        r = requests.get('https://sandbox.original.com.br/cards/v1', headers=self.headers)
        if r.status_code == 200:
            datum = r.json()
            for data in datum:
                self.cards.append(data)
            return self.cards
        else:
            return []

    def get_auth(self):
        r = requests.get('{0}?scopes={1}&callback_url={2}&developer_key={3}'.format(URL, SCOPES, CALLBACK_URL, self.developer_key))

    def callback_auth():
        pass
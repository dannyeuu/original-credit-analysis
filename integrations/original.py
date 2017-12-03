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

    def limits(self):
        r = requests.get('https://sandbox.original.com.br/accounts/v1/balance', headers=self.headers)
        if r.status_code == 200:
            data = r.json()
            self.current_balance = float(data['current_balance'])
            self.available_limit = float(data['available_limit'])
            self.current_limit = float(data['current_limit'])
            return self.current_balance, self.available_limit, self.current_limit
        else:
            return 10000.00, 5000.0, 15000.00
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = 'original-credit-analysis'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\xcagC\xac\x0e]lTY2\xd2\x9fS\xa2[#\xcfA\x0c6\x9c|\xcbs\\\xb6\xd3\xa1Q/\x8b\xd1F\x8f.se\xee\x91!\xfd\xb3\xa7\xe79\xb4\x0e\xc9'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI
    KERAS_MODEL_FILE = basedir + 'model.h5'
    
    # Original Integration
    ORIGINAL_API_URL = 'https://sandbox.original.com.br'
    ORIGINAL_AUTH_URL = 'https://sb-autenticacao-api.original.com.br'
    ORIGINAL_AUTH_CALLBACK_URL = 'http://localhost:5000/callback'
    ORIGINAL_DEVELOPER_KEY = '28f955c90b3a2940134ff1a970050f569a87facf'
    ORIGINAL_SECRET_KEY = 'dd385cd0b59c013560400050569a7fac'
    ORIGINAL_ACCESS_TOKEN = 'Bearer YjU1NmRmZDAtZDdjOC0xMWU3LWJjNTEtMDA1MDU2OWE3MzA1OmV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUowZVhCbElqb2lUMEYxZEdnaUxDSnBZWFFpT2pFMU1USXlOalF6TlRZc0ltVjRjQ0k2TVRVeE1qWTVOak0xTml3aVlYVmtJam9pTldJMFpqZG1PR1lpTENKcGMzTWlPaUphZFhBdWJXVWdSMkYwWlhkaGVTSXNJbk4xWWlJNkltSTFOVFprWm1Rd0xXUTNZemd0TVRGbE55MWlZelV4TFRBd05UQTFOamxoTnpNd05TSXNJbXAwYVNJNkltVTVNR0ZqWlRRd0xXUTNZemd0TVRGbE55MWhOMk13TFdNeE56WXlaRFl3TlRRME5pSjkuOGxUcjUtWmpSVFFxN0pTTDZueHA3SEt1bVBjQ0RtZ0dGZ0FOaDdNSG9ibw=='

    # Foursquare Integration
    SOCIAL_FOURSQUARE = {
        'consumer_key': 'VMB5XEAGSGGDCPIQ3KUWW5CMV4T0LPY3XUX2RPNNC14AC1NT',
        'consumer_secret': 'QPEREZMKSIIT3NBTMVMCZOSOA4EAOMSQHWLCDPF0UN4W2F34'
    }
    # Faccebook Integration
    SOCIAL_FACEBOOK = {
        'consumer_key': '135017777116915',
        'consumer_secret': '4d92534b11f3b6227561494b3c2a943f'
    }

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://jmrzzlhsywytsq:90fe8cf47c70789209b0f2c6cb66a982f6ee4348ef154ac105871255548274a3@ec2-107-21-205-25.compute-1.amazonaws.com:5432/d3avcgp8o7hi9g'
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


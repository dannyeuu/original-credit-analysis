#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\xcagC\xac\x0e]lTY2\xd2\x9fS\xa2[#\xcfA\x0c6\x9c|\xcbs\\\xb6\xd3\xa1Q/\x8b\xd1F\x8f.se\xee\x91!\xfd\xb3\xa7\xe79\xb4\x0e\xc9'
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Original Integration
    ORIGINAL_API_URL = 'https://sandbox.original.com.br'
    ORIGINAL_AUTH_URL = 'https://sb-autenticacao-api.original.com.br'
    ORIGINAL_AUTH_CALLBACK_URL = 'http://localhost:5000/callback'
    ORIGINAL_DEVELOPER_KEY = '28f955c90b3a2940134ff1a970050f569a87facf'
    ORIGINAL_SECRET_KEY = 'dd385cd0b59c013560400050569a7fac'
    ORIGINAL_ACCESS_TOKEN = 'Bearer MzA0MThkOTAtZDdiZS0xMWU3LWJjNTEtMDA1MDU2OWE3MzA1OmV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUowZVhCbElqb2lUMEYxZEdnaUxDSnBZWFFpT2pFMU1USXlOVGszTnpnc0ltVjRjQ0k2TVRVeE1qWTVNVGMzT0N3aVlYVmtJam9pTldJMFpqZG1PR1lpTENKcGMzTWlPaUphZFhBdWJXVWdSMkYwWlhkaGVTSXNJbk4xWWlJNklqTXdOREU0WkRrd0xXUTNZbVV0TVRGbE55MWlZelV4TFRBd05UQTFOamxoTnpNd05TSXNJbXAwYVNJNklqUXdOemd4T0dFd0xXUTNZbVV0TVRGbE55MWhOMk13TFdNeE56WXlaRFl3TlRRME5pSjkuc0lrVmFrby15WnZWNDR5Q1cwem5wTVdLM1pueFhJUGs3RlZVV2tuQmVXWQ=='


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


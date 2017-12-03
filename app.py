#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, request
from flask import send_from_directory


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()

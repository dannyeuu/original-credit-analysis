#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, request, Response
from flask import send_from_directory
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
login_manager = LoginManager(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



@app.route('/')
def hello():
    response = app.response_class(
            response=json.dumps({'status_code': 200}),
            status=200,
            mimetype='application/json'
        )
    return response

@app.route('/import/original/invoices', methods=['GET'])
def import_original_invoices():
	pass

if __name__ == '__main__':
    app.run()

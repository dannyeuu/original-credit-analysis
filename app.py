#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
import urllib
from flask import Flask, request, Response, session
from flask import send_from_directory, g
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user 

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from models import *
from utils import *
from integrations.original import OriginalIntegration


# Override the default handlers with JSON responses
# @app.errorhandler(400)
# def forbidden(error):
#     """
#     Renders 400 response
#     :returns: JSON
#     :rtype: flask.Response
#     """
#     response = app.response_class(
#         response='Error 400: Bad request',
#         status=400,
#         mimetype='application/json'
#     )
#     return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/user/add', methods=['POST'])
def user_add():
    data = request.json
    name = data['name']
    cpf = data['cpf']
    password = bcrypt.generate_password_hash(data['password'])

    # Verify if the cpf has already on
    if User.query.filter_by(cpf=cpf).first() is not None:
        response = app.response_class(
            response=json.dumps({'description': 'cpf already exists'}),
            status=409,
            mimetype='application/json'
        )
        return response

    # Try to insert User
    user = User(name=name, cpf=cpf, password=password)
    db.session.add(user)
    if db.session.commit():
        response = app.response_class(
            response=json.dumps({'name': name, 'cpf':cpf}),
            status=200,
            mimetype='application/json'
        )
    # On error log
    else:
        db.session.rollback()
        response = app.response_class(
            response=json.dumps({'status_code': 500}),
            status=500,
            mimetype='application/json'
        )

    return response

@app.route('/integrations/original/add', methods=['POST'])
# @login_required
def integrations_original_add():
    data = request.json
    access_token = data['access_token']
    integration = Integration.query.filter_by(access_token=app.config['ORIGINAL_ACCESS_TOKEN'], provider_name='original').first()
    
    try:
        access_token = integration.access_token
    except:
        response = app.response_class(
            response=json.dumps({'description': 'missing access_token for user: {0}'.format(load_user().email)}),
            status=409,
            mimetype='application/json'
        )
        return response

    integration = OriginalIntegration(user_id=user_id, access_token=app.config['ORIGINAL_ACCESS_TOKEN'], developer_key=app.config['developer_key'])
    cards = integration.import_original_cards()

    for card in cards:
        new_card = get_or_create(
            db.session,
            Card,
            number=card['number'],
            card_type=card['card_type'],
            expire_year=card['expire_year'],
            expire_month=card['expire_month'],
            direct_debit=card['direct_debit'],
            purchase_limit=card['purchase_limit'],
            available_limit=card['available_limit'],
            spent=card['spent'],
            payment_day=card['payment_day'],
            user_id=card['user_id'],
        )

    response = app.response_class(
        response=json.dumps({'description': 'missing access_token for user: {0}'.format(load_user().email)}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/predict', methods=['POST'])
# @login_required
def predict():
    data = request.json
    user_id = load_user().id
    integration = Integration.query.filter_by(user_id=user_id, provider_name='original').first()
    
    try:
        access_token = integration.access_token
    except:
        response = app.response_class(
            response=json.dumps({'description': 'missing access_token for user: {0}'.format(load_user().email)}),
            status=409,
            mimetype='application/json'
        )
        return response
    

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/consulta-credito.html', methods=['POST'])
def login():
    data = request.form
    # email = data['email']
    cpf = data['cpf']
    password = data['password']

    user = User.query.filter_by(cpf=cpf).first()
    if user is not None:
        pw_hash = bcrypt.generate_password_hash(password)
        if bcrypt.check_password_hash(pw_hash, password):
            login_user(user)
            session['name'] = user.name
            session['cpf'] = user.cpf
            session['id'] = user.id
            # response = app.response_class(
            #             response=json.dumps({'status_code': 200}),
            #             status=200,
            #             mimetype='application/json'
            #         )
            # return response
            current_balance, available_limit, current_limit = balance(user_id=session['id'], access_token=app.config['ORIGINAL_ACCESS_TOKEN'])
            return render_template('consultaCredito.html', name=session['name'], current_balance=current_balance, available_limit=current_balance, current_limit=current_limit)
    # response = app.response_class(
    #     response=json.dumps({'description': 'user or password are incorrect'}),
    #     status=401,
    #     mimetype='application/json'
    # )
    # return response


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/acesso-conta')
def acesso_conta():
    return render_template('acessoConta.html')

@app.route('/melhora-credito')
def melhora_credito():
    current_balance, available_limit, current_limit = balance(user_id=session['id'], access_token=app.config['ORIGINAL_ACCESS_TOKEN'])
    return render_template('melhoraCredito.html', name=session['id'], current_balance=current_balance, available_limit=current_balance, current_limit=current_limit)

def balance(user_id, access_token):
    integration = OriginalIntegration(user_id=session['id'], access_token=app.config['ORIGINAL_ACCESS_TOKEN'], developer_key=app.config['ORIGINAL_DEVELOPER_KEY'])
    current_balance, available_limit, current_limit = integration.limits()
    return current_balance, available_limit, current_limit

def predict_credit():
    pass

if __name__ == '__main__':
    app.run()
    model = load_ml_model()

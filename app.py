#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, request, Response
from flask import send_from_directory, g
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user 


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from models import *
from integrations.original import OriginalIntegration

# Override the default handlers with JSON responses
@app.errorhandler(400)
def forbidden(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 400: Bad request",
            success=False,
            data=None
        )
    ), 400

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/user/add', methods=['POST'])
def user_add():
    data = request.json
    name = data['name']
    email = data['email']
    password = pw_hash = bcrypt.generate_password_hash(data['password'])

    # Verify if the email has already on
    if User.query.filter_by(email=email) is not None:
        response = app.response_class(
            response=json.dumps({'description': 'email already exists'}),
            status=409,
            mimetype='application/json'
        )
        return response

    # Try to insert User
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    if db.session.commit():
        response = app.response_class(
            response=json.dumps({'name': name, 'email':email}),
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

    integration = OriginalIntegration(user_id=user_id, access_token=access_token, developer_key=app.config['developer_key'])
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

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user is not None:
        pw_hash = bcrypt.generate_password_hash(password)
        if bcrypt.check_password_hash(pw_hash, password):
            login_user(user)
            response = app.response_class(
                        response=json.dumps({'status_code': 200}),
                        status=200,
                        mimetype='application/json'
                    )
            return response
    response = app.response_class(
        response=json.dumps({'description': 'user or password are incorrect'}),
        status=401,
        mimetype='application/json'
    )
    return response


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    response = app.response_class(
            response=json.dumps({'status_code': 200}),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/')
def hello():
    response = app.response_class(
            response=json.dumps({'status_code': 200}),
            status=200,
            mimetype='application/json'
        )
    return response


if __name__ == '__main__':
    app.run()

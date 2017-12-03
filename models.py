#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from app import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    cpf = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120), unique=False)
    is_active = db.Column(db.Boolean, unique=False)
    token = db.Column(db.String(120), unique=False)
    expire = db.Column(db.TIMESTAMP, unique=False)

    def __init__(self, name, password, cpf):
        self.name = name
        self.cpf = cpf  
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.name

class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(80), unique=False)
    access_token = db.Column(db.String, unique=True)
    client_id = db.Column(db.String, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __init__(self, provider_name, access_token, user_id):
        self.provider_name = provider_name
        self.access_token = access_token
        self.user_id = user_id

    def __repr__(self):
        return '<Integration %r>' % self.provider_name


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(8), unique=False)
    card_type = db.Column(db.String(50), unique=False)
    expire_year = db.Column(db.Integer, unique=False)
    expire_month = db.Column(db.Integer, unique=False)
    direct_debit = db.Column(db.Boolean, unique=False)
    purchase_limit = db.Column(db.DECIMAL(18,2), unique=False)
    available_limit = db.Column(db.DECIMAL(18,2), unique=False)
    spent = db.Column(db.DECIMAL(18,2), unique=False)
    payment_day = db.Column(db.DECIMAL(18,2), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __init__(self, number, card_type, expire_year, 
                expire_month, direct_debit, purchase_limit, 
                available_limit, spent, payment_day, user_id):
        self.number = number
        self.card_type = card_type
        self.expire_year = expire_year
        self.expire_month = expire_month
        self.direct_debit = direct_debit
        self.purchase_limit = purchase_limit
        self.available_limit = available_limit
        self.spent = spent
        self.payment_day = payment_day
        self.user_id = user_id

    def __repr__(self):
        return '<Card %r>' % self.number


class OriginalInvoicesHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dollar  = db.Column(db.DECIMAL(18,2), unique=True)
    amount  = db.Column(db.DECIMAL(18,2), unique=True)
    previous_amount  = db.Column(db.DECIMAL(18,2), unique=True)
    total_credits  = db.Column(db.DECIMAL(18,2), unique=True)
    total_debits  = db.Column(db.DECIMAL(18,2), unique=True)
    payment_date  = db.Column(db.DATE, unique=True)
    effective_monthly_rate  = db.Column(db.DECIMAL(18,2), unique=True)
    effective_yearly_rate  = db.Column(db.DECIMAL(18,2), unique=True)
    rotational_rate  = db.Column(db.DECIMAL(18,2), unique=True)
    rotational_cash_rate  = db.Column(db.DECIMAL(18,2), unique=True)
    fine_rate  = db.Column(db.DECIMAL(18,2), unique=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'),
        nullable=False)

    def __init__(self, dollar, amount, previous_amount, 
                total_credits, total_debits, payment_date, 
                effective_monthly_rate, effective_yearly_rate, 
                rotational_rate, rotational_cash_rate, fine_rate):
        self.dollar = dollar
        self.amount = amount
        self.previous_amount = previous_amount
        self.total_credits = total_credits
        self.total_debits = total_debits
        self.payment_date = payment_date
        self.effective_monthly_rate = effective_monthly_rate
        self.effective_yearly_rate = effective_yearly_rate
        self.rotational_rate = rotational_rate
        self.rotational_cash_rate = rotational_cash_rate
        self.fine_rate = fine_rate

    def __repr__(self):
        return '<OriginalInvoicesHistory %r>' % self.id


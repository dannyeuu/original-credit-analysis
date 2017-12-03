#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keras.models import model_from_json
import numpy as np

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

# load json and create model
def load_ml_model():
    json_file = open('model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights("model.h5")
    return model

# Patametric variation
def bissecao(model, X):
    n = len(X)
    a = X[0]
    ca = model.predict_classes(np.reshape(X, [1, n]))
    b = 2*a
    X[0] = b

    # encontra o primeiro valor a cruzar o zero
    cb = model.predict_classes(np.reshape(X, [1, n]))
    if cb == 1:
        i = 0
        while cb == 1 and i <= 2: # enquanto for pagador
            b = 2*b
            X[0] = b
            cb = model.predict_classes(np.reshape(X, [1, n]))
            i += 1
        if cb == 1 and i == 3:
            return a, b # não queremos aumentar tanto assim o limite
    else:
        i = 0
        while ca == 0 and a > 1.:
            a = a/2
            X[0] = a
            ca = model.predict_classes(np.reshape(X, [1,n]))
            i += 1
        if ca == 0:
            return a, b


    i = 0
    while ((b - a) >= 10) and i < 50:
        p = a + (b-a)/2
        cp = model.predict_classes(np.reshape(X, [1, n]))
        if ca == 1 and cp == 1 or ca == 0 and cp == 0:
            a = p
            ca = cp
        else:
            b = p
            X[0] = b
        i += 1

    return a, b

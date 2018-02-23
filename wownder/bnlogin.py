# -*- coding: utf-8 -*-
import random
import requests

from functools import wraps

from flask import abort, session, request, redirect, jsonify, current_app as app
from flask_login import login_user, logout_user, current_user
from werkzeug.exceptions import Unauthorized

from wownder import db
from wownder.actions import update_user, update_chars
from wownder import tasks


AUTH_URI = 'https://us.battle.net/oauth/authorize'
TOKEN_URI = 'https://us.battle.net/oauth/token'


def _gen_state(n=10):
    _alpha = 'abcdefghijlmnopqrstuvxzwykABCDEFGHIJLMNOPQRSTUVXZWYK1234567890'
    return ''.join(random.choice(_alpha) for _ in range(n))


def login_url(state=None):
    _state = state if state else _gen_state(11)
    _url = (AUTH_URI +
            "?client_id=" + app.config['BN_CLIENT_ID'] + "&"
            "response_type=code&"
            "redirect_uri=" + request.host_url + "oauth/callback&"
            "scope=wow.profile&"
            "state={}").format(_state)
    return _url


def _auth():
    _state = _gen_state(11)
    session['state'] = _state
    return redirect(login_url(_state))


def requires_bn_login_api(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify(dict(url=login_url())), 401
        try:
            return func(*args, **kwargs)
        except Unauthorized:
            return jsonify(dict(url=login_url())), 401
    return func_wrapper


def handle_callback():
    if 'error' in request.args:
        return 'ERROR: %s' % request.args.get('error')

    _code = request.args['code']
    if session.get('state') != request.args['state']:
        #  TODO: Possible security issue. Handle it.
        pass
    _payload = {
        'grant_type': 'authorization_code',
        'code': _code,
        'redirect_uri': request.host_url + "oauth/callback",
        'client_id': app.config['BN_CLIENT_ID'],
        'client_secret': app.config['BN_SECRET']
    }

    _resp = requests.post(TOKEN_URI, data=_payload)
    if _resp.status_code != 200:
        # TODO: Log _resp.json here!
        abort(_resp.status_code)
    _json = _resp.json()
    oauth_token = _json['access_token']
    user = update_user(oauth_token)
    update_chars(user, 'us')
    update_chars(user, 'eu')
    db.session.add(user)
    db.session.commit()
    login_user(user)
    tasks.update_chars.delay(user.id)

    return redirect(app.config.get("SITE_URL"))

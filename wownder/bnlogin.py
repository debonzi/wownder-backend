# -*- coding: utf-8 -*-
import random
import requests

from functools import wraps

from flask import abort, session, request, redirect, jsonify, current_app as app
from flask_login import login_user, current_user
from werkzeug.exceptions import Unauthorized

from wownder import db
from wownder.actions import update_user, update_chars
from wownder import tasks


ENDPOINTS = {
    'US': {
        'AUTH_URI': 'https://us.battle.net/oauth/authorize',
        'TOKEN_URI': 'https://us.battle.net/oauth/token'
    },
    'EU': {
        'AUTH_URI': 'https://eu.battle.net/oauth/authorize',
        'TOKEN_URI': 'https://eu.battle.net/oauth/token'
    }
}


def _gen_state(n=10):
    _alpha = 'abcdefghijlmnopqrstuvxzwykABCDEFGHIJLMNOPQRSTUVXZWYK1234567890'
    return ''.join(random.choice(_alpha) for _ in range(n))


def _get_path():
    _state = _gen_state(11)
    session['state'] = _state
    path = ("?client_id=" + app.config['BN_CLIENT_ID'] + "&"
            "response_type=code&"
            "redirect_uri=" + request.host_url + "oauth/callback&"
            "scope=wow.profile&"
            "state={}").format(_state)
    return path


def us_login_url():
    return ENDPOINTS.get('US').get('AUTH_URI') + _get_path()


def eu_login_url():
    return ENDPOINTS.get('EU').get('AUTH_URI') + _get_path()


def requires_bn_login_api(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify(), 401
        try:
            return func(*args, **kwargs)
        except Unauthorized:
            return jsonify(), 401
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

    _resp = requests.post(ENDPOINTS.get(session.get('login_region')).get('TOKEN_URI'), data=_payload)
    if _resp.status_code != 200:
        # TODO: Log _resp.json here!
        abort(_resp.status_code)
    _json = _resp.json()
    oauth_token = _json['access_token']
    user = update_chars(update_user(oauth_token))
    db.session.add(user)
    db.session.commit()
    login_user(user)
    tasks.update_chars.delay(user.id)

    return redirect(app.config.get("SITE_URL"))

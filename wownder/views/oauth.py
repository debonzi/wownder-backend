# -*- coding: utf-8 -*-
from flask import Blueprint

from wownder.bnlogin import handle_callback


oauth = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth.route('/callback')
def callback():
    return handle_callback()

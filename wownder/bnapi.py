# -*- coding: utf-8 -*-
import requests
from flask import abort


def get_request(url):
    _resp = requests.get(url)
    return _resp.json() if _resp.ok else abort(_resp.status_code)


# User Battlenet API
def get_user_info(token):
    _url = 'https://us.api.battle.net/account/user?access_token={}'.format(token)
    return get_request(_url)


def get_user_chars(token, region):
    _url = 'https://{}.api.battle.net/wow/user/characters?access_token={}'.format(region, token)
    return get_request(_url)


def _get_char(apikey, region, realm, name, fields=None):
    _url = ('https://%s.api.battle.net/wow/character/%s/%s?locale=en_US&apikey=%s'
            % (region, realm, name, apikey))
    if fields:
        _fields = '&fields='
        for f in fields:
            _fields += "%s," % f
        _url += _fields
    return get_request(_url)


def get_char(apikey, region, realm, name):
    return _get_char(apikey, region, realm, name)


def get_char_pvp(apikey, region, realm, name):
    return _get_char(apikey, region, realm, name, ('pvp',))


def get_char_stats(apikey, region, realm, name):
    return _get_char(apikey, region, realm, name, ('statistics',))


def get_char_pvp_stats(apikey, region, realm, name):
    return _get_char(apikey, region, realm, name, ('pvp', 'statistics'))

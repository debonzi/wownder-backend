# -*- coding: utf-8 -*-
from wownder import db
from wownder.bnapi import get_user_info, get_user_chars
from wownder.models import User, Char, PvPCharStats


def update_user(oauth_token):
    user_info = get_user_info(oauth_token)
    _user = User.create_or_update(bn_id=user_info['id'],
                                  battletag=user_info['battletag'],
                                  oauth_token=oauth_token)

    return _user


def remove_char(char):
    PvPCharStats.remove_from_char(char)  # TODO: Test Char delete when there is Stats
    db.session.delete(char)


def update_chars(user, region):
    _chars = get_user_chars(user.oauth_token, region)
    for char in _chars['characters']:
        user.chars.append(Char.create_or_update(char, region, enforce_user_id=user.id))

    # Check if all chars still exists on BN
    remove = []
    for _c in user.chars.filter_by(region=region):
        found = False
        for char_info in _chars['characters']:
            if all([char_info['name'] == _c.name, char_info['realm'] == _c.realm, _c.region == region]):
                found = True
        if not found:
            remove.append(_c)
    [remove_char(_c) for _c in remove]
    return user

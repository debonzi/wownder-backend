# -*- coding: utf-8 -*-
import json, sys
from . import ConfigBase


def _get_dev_credenditials():
    with open("bnet-devel.json") as fp:
        credentials = json.load(fp)
    return credentials


class Config(ConfigBase):
    try:
        credentials = _get_dev_credenditials()
        BN_CLIENT_ID = credentials.get("BN_CLIENT_ID")
        BN_SECRET = credentials.get("BN_SECRET")
    except Exception as exc:
        print(
            """
            Error reading development bnet credentials."

            please, create a bnet-devel.json file at project root with the following format:

            {
                "BN_CLIENT_ID": "<BNET APP KEY>",
                "BN_SECRET": "<BNET APP SECRET>"
            }
            """
        )
        sys.exit(1)

    DEBUG = True
    SECRET_KEY = 'changethissecret'
    SQLALCHEMY_DATABASE_URI = 'postgres://wownder:wownder@127.0.0.1/wownder'

    CORS_ORIGIN = "http://localhost:3000"
    SITE_URL = "http://localhost:3000"

    BROKER_URL = 'redis://localhost:6379/5'

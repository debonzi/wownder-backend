# -*- encoding: utf-8 -*-
import os
from kombu import Exchange, Queue


_queues_names = (
    'char_update',
)


class ConfigBase(object):
    DEBUG = False
    TESTING = False
    BN_CLIENT_ID = os.getenv("BN_CLIENT_ID")
    BN_SECRET = os.getenv("BN_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN = os.getenv("CORS_ORIGIN")
    SITE_URL = os.getenv("SITE_URL")

    BROKER_URL = "{}/0".format(os.getenv('REDIS_URL'))
    CELERY_QUEUES = [
        Queue(name, Exchange(name), routing_key=name) for name in _queues_names
        ]



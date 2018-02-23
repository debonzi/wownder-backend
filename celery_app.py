# -*- encoding: utf-8 -*-
from wownder import create_app, celery_app

from raven import Client
from raven.contrib.celery import register_signal

flask_app = create_app()
register_signal(Client())

application = celery_app

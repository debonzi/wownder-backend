# -*- coding: utf-8 -*-
import os
import celery

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from raven.contrib.flask import Sentry

from werkzeug.exceptions import NotFound, Forbidden, default_exceptions

#  https://<region>.battle.net/oauth/authorize
#  https://<region>.battle.net/oauth/token


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
celery_app = celery.Celery()
sentry = Sentry()


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')):
    app = Flask(__name__)

    app.config.from_object('wownder.config.%s.Config' % config_var.lower())

    sentry.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery.Task.__call__(self, *args, **kwargs)

    celery_app.conf.update(app.config)
    celery_app.Task = ContextTask

    def _error_handling(e):
        if isinstance(e, NotFound):
            return jsonify({}), 404
        elif isinstance(e, Forbidden):
            return jsonify({}), Forbidden.code
        return jsonify({}), e.code if hasattr(e, 'code') else 500

    for _code in default_exceptions.keys():
        app.errorhandler(_code)(_error_handling)

    from wownder.views.oauth import oauth
    app.register_blueprint(oauth)

    from wownder.views.api import api
    app.register_blueprint(api)

    return app

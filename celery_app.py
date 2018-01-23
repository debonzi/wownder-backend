# -*- encoding: utf-8 -*-
from wownder import create_app, celery_app

flask_app = create_app()
application = celery_app

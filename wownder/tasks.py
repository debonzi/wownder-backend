# -*- encoding: utf-8 -*-
from flask import current_app as app
from werkzeug.exceptions import NotFound


from wownder import celery_app, bnapi, db

from wownder.models import Char, User


@celery_app.task(name="chars_update_dispatcher_task", queue="char_update")
def update_chars(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return

    for char in user.chars:
        if char.level < 110:
            continue
        update_char.delay(char.uuid)


@celery_app.task(name="char_update_task", queue="char_update")
def update_char(char_uuid):
    char = Char.query.filter_by(uuid=char_uuid).first()
    if not char:
        return
    try:
        _char = bnapi.get_char_pvp_stats(app.config['BN_CLIENT_ID'], char.region, char.realm, char.name)
    except Exception as e:
        if isinstance(e, NotFound):
            # app.logger.info('Char %s-%s not found on Battlenet' % (char.name, char.realm))
            _char = None  # This will make current stats equal 0
        pass

    char.create_or_update_stats(_char)
    db.session.add(char)
    db.session.commit()

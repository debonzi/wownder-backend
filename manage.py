#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import MigrateCommand

from wownder import create_app, db

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


@manager.command
def about():
    print("The WoW Society.")


@manager.command
def init_db():
    db.drop_all()
    db.create_all()


@manager.command
def uuid():
    import uuid
    from wownder.models import Char

    for c in Char.query:
        if not c.uuid:
            c.uuid = uuid.uuid4().hex
            db.session.add(c)
    db.session.commit()


@manager.command
def hall():
    from wownder.models import PvPCharStats
    _hall = PvPCharStats.get_hall()
    for b, h in _hall:
        print(b)
        for c in h:
            print(c.char.name)


@manager.command
def cevent():
    from wownder import db
    from wownder.models.wowevents import WowEvent, EventSubscribers
    from wownder.models import Char
    from datetime import datetime

    we = WowEvent.query.first()
    if not we:
        now = datetime.utcnow()
        we = WowEvent(type='ARENA2', start_time=now, owner_id=9, updated_at=now, created_at=now)
        db.session.add(we)
        db.session.commit()
    print(we.owner)
    if not we.subscribers:
        _c = Char.query.get(9)
        we.add_subscriber(_c)
        db.session.add(we)
        db.session.commit()
    # import pdb;pdb.set_trace()
    # print we.chars[0].char.name, we.chars[0].status
    # print we.owner.events[0].event.title



if __name__ == '__main__':
    manager.run()


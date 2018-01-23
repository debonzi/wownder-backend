# -*- coding: utf-8 -*-
from flask_login import UserMixin

from wownder import db, login_manager
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

__all__ = ['User']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    battletag = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    oauth_token = db.Column(db.String(50))
    language = db.Column(db.String(5), nullable=False, default='pt')

    chars = relationship("Char", backref='user', order_by="desc(Char.level)",
                         primaryjoin="and_(User.id == Char.user_id, Char.level == 110)",
                         lazy='dynamic')

    @classmethod
    def create_or_update(cls, bn_id, battletag, oauth_token):
        user = cls.query.get(bn_id)
        if not user:
            return cls(id=bn_id, battletag=battletag, oauth_token=oauth_token)
        user.battletag = battletag
        user.oauth_token = oauth_token
        return user

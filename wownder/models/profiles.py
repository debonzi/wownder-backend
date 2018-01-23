# -*- coding: utf-8 -*-
import datetime
from wownder import db


__all__ = ['Profile']


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    char_id = db.Column(db.Integer, db.ForeignKey("char.id"), index=True, nullable=False)
    role = db.Column(db.String(20), index=True, nullable=False, default="DPS")
    faction = db.Column(db.String(10), index=True, nullable=False)
    listed_2s = db.Column(db.Boolean, nullable=False, index=True, default=False)
    listed_3s = db.Column(db.Boolean, nullable=False, index=True, default=False)
    voice = db.Column(db.Boolean, nullable=False, index=True, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           nullable=False)

    char = db.relationship("Char", back_populates="profile")

    @classmethod
    def create_for_char(cls, char, **kwargs):
        kwargs.update(dict(char=char, faction=char.faction))
        return cls(**kwargs)

    def __iter__(self):
        yield "role", self.role
        yield "faction", self.faction
        yield "listed_2s", self.listed_2s
        yield "listed_3s", self.listed_3s
        yield "voice", self.voice
        yield "char_uuid", self.char.uuid

# -*- coding: utf-8 -*-
import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.orm import relationship

from wownder import db
from wownder import enums


__all__ = ['Char', 'PvPCharStats']


class Char(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(33), index=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    name = db.Column(db.String(30))
    realm = db.Column(db.String(30))
    char_class = db.Column(db.SmallInteger)
    race = db.Column(db.SmallInteger)
    gender = db.Column(db.SmallInteger)
    level = db.Column(db.SmallInteger)
    thumbnail = db.Column(db.String(255))
    last_bn_update = db.Column(db.DateTime)
    region = db.Column(db.String(2), nullable=False, index=True, default='us')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           nullable=False)
    __table_args__ = (db.Index('char_name_realm_region_un', name, realm, region, unique=True),)

    stats = relationship("PvPCharStats", backref='char', uselist=False)
    profile = relationship("Profile", uselist=False, back_populates="char")
    chat_rooms = relationship("ChatRoom",
                              primaryjoin="or_(Char.id == ChatRoom.char_1_id, Char.id == ChatRoom.char_2_id)",
                              lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(Char, self).__init__(*args, **kwargs)
        if not self.uuid:
            self.uuid = uuid.uuid4().hex

    @classmethod
    def by_realm_name(cls, realm, name):
        return cls.query.filter(func.lower(cls.realm) == realm.lower(),
                                func.lower(cls.name) == name.lower()).first()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def create_or_update(cls, char_info, region, enforce_user_id=None):
        _char = cls.query.filter_by(name=char_info['name'],
                                    realm=char_info['realm'],
                                    region=region).first()

        if enforce_user_id and _char and _char.user_id != enforce_user_id:
            # The char exists under someones else User.
            # Probably DELETED from an account and created under another account
            from wownder.actions import remove_char
            remove_char(_char)
            _char = None

        if not _char:
            return cls(name=char_info['name'],
                       realm=char_info['realm'],
                       char_class=char_info['class'],
                       race=char_info['race'],
                       gender=char_info['gender'],
                       level=char_info['level'],
                       thumbnail=char_info['thumbnail'],
                       last_bn_update=datetime.datetime.fromtimestamp(char_info['lastModified']/1000),
                       uuid=uuid.uuid4().hex,
                       region=region
                       )
        _char.level = char_info['level']
        _char.thumbnail = char_info['thumbnail']
        _char.last_bn_update = datetime.datetime.fromtimestamp(char_info['lastModified']/1000)
        return _char

    def create_or_update_stats(self, char_stats):
        if not self.stats:
            self.stats = PvPCharStats()

        if not char_stats:
            self.stats.b2_current_rating = 0
            self.stats.b3_current_rating = 0
            self.stats.rbg_current_rating = 0
            self.updated_at = datetime.datetime.utcnow()
            return

        for _sst in char_stats['statistics']['subCategories']:
            if _sst["id"] == 21:  # PvP
                _pvp_subs = _sst['subCategories']
                break
        for _arenas_s in _pvp_subs:
            if _arenas_s['id'] == 152:  # Ranked Arenas
                _arenas = _arenas_s['statistics']
                break

        _best_2 = 0
        _best_3 = 0
        for _pvp_s in _arenas:
            if _pvp_s["id"] == 595:  # Best 3s
                _best_3 = _pvp_s["quantity"]
            elif _pvp_s["id"] == 370:  # Best 2s
                _best_2 = _pvp_s["quantity"]
            if _best_3 and _best_2:
                break

        self.stats.b2_best_rating = _best_2
        self.stats.b3_best_rating = _best_3
        self.stats.b2_current_rating = char_stats['pvp']['brackets']['ARENA_BRACKET_2v2']['rating']
        self.stats.b3_current_rating = char_stats['pvp']['brackets']['ARENA_BRACKET_3v3']['rating']
        self.stats.rbg_current_rating = char_stats['pvp']['brackets']['ARENA_BRACKET_RBG']['rating']
        self.updated_at = datetime.datetime.utcnow()
        self.level = char_stats['level']
        self.thumbnail = char_stats['thumbnail']
        self.last_bn_update = datetime.datetime.fromtimestamp(char_stats['lastModified']/1000)

    @property
    def faction(self):
        return enums.RACE_TO_FACTION.get(self.race)

    @property
    def c_class(self):
        return enums.CLASS.get(self.char_class)

    @property
    def h_labels(self):
        labels = [str(h.created_at.date()) for h in self.history]
        # if labels:
        #     labels[0], labels[-1] = str(self.history[0].created_at.date()), str(self.history[-1].created_at.date())
        return str(labels)

    @property
    def h2_series(self):
        return str([int(h.b2_rating) for h in self.history])

    @property
    def h3_series(self):
        return str([int(h.b3_rating) for h in self.history])

    @property
    def hbg_series(self):
        return str([int(h.rbg_rating) for h in self.history])

    @property
    def thumbnail_url(self):
        return (
            "https://render-us.worldofwarcraft.com/character/%s?alt=wow/static/images/2d/avatar/%s-%s.jpg"
            % (self.thumbnail, self.race, self.gender)
        )

    @property
    def profile_url(self):
        return (
            "https://render-us.worldofwarcraft.com/character/%s?alt=wow/static/images/2d/profilemain/race/%s-%s.jpg"
            % (self.thumbnail.replace('avatar', 'main'), self.race, self.gender)
        )

    @property
    def inset_url(self):
        return (
            "https://render-us.worldofwarcraft.com/character/%s?alt=wow/static/images/2d/inset/%s-%s.jpg"
            % (self.thumbnail.replace('avatar', 'inset'), self.race, self.gender)
        )

    def __iter__(self):
        yield "uuid", self.uuid
        yield "name", self.name
        yield "class", self.c_class
        yield "realm", self.realm
        yield "level", self.level
        yield "s2_cr", self.stats.b2_current_rating if self.stats else 0
        yield "s3_cr", self.stats.b3_current_rating if self.stats else 0
        yield "inset_url", self.inset_url
        yield "profile_url", self.profile_url
        yield "thumbnail_url", self.thumbnail_url
        yield "race", enums.RACE[self.race]
        yield "region", self.region


class PvPCharStats(db.Model):
    __tablename__ = 'pvp_char_stats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    char_id = db.Column(db.Integer, db.ForeignKey('char.id'), index=True)
    b2_current_rating = db.Column(db.Integer, nullable=False, default=0, index=True)
    b3_current_rating = db.Column(db.Integer, nullable=False, default=0, index=True)
    b2_best_rating = db.Column(db.Integer, nullable=False, default=0)
    b3_best_rating = db.Column(db.Integer, nullable=False, default=0)
    rbg_current_rating = db.Column(db.Integer, nullable=False, default=0, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           nullable=False)

    @classmethod
    def remove_from_char(cls, char):
        cls.query.filter_by(char_id=char.id).delete()

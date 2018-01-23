# -*- coding: utf-8 -*-
from . import ConfigBase


class Config(ConfigBase):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://wownder:wownder@127.0.0.1/wownder_test'

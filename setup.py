# -*- coding: utf-8 -*-
from setuptools import setup

requires = [
    'Flask==0.12.2',
    'Flask-Babel==0.11.2',
    'Flask-WTF==0.14.2',
    'Flask-SQLAlchemy==2.3.2',
    'Flask-Migrate==2.1.1',
    'Flask-Login==0.4.1',
    'psycopg2==2.7.3.2',
    'SQLAlchemy-Utils==0.32.21',
    'colander==1.4',
    "celery[redis]==4.1.0",
]

extras_require = {
    'test': [
        'pytest-flask>=0.10.0'
    ],
}

setup(name='wownder',
      version='0.0.1',
      description='WoW PvP Match up',
      author='Daniel Debonzi',
      author_email='debonzi@gmail.com',
      install_requires=requires,
      extras_require=extras_require,
      url='https://bitbucket.org/debonzi/wownder',
      packages=['wownder'],
      )

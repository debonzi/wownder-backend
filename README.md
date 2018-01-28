# wownder-backend

## What is it?
wownder-backend is a simple "Arena Match Finder" for people who plays World of Warcraft Arenas and wants to have a place to find Arena partners.
It is just the backend side of the application. You can find the frontend repository at https://github.com/debonzi/wownder-frontend

## What is its status?
It is on really early development stage. The core functions (find matches and messages) are very functional but very basic. They should be evolving on next commits.


```bash
sudo su - postgres
psql

> DROP DATABASE IF EXISTS wownder;
> CREATE DATABASE wownder;
> CREATE ROLE wownder WITH LOGIN PASSWORD 'wownder';
> GRANT ALL PRIVILEGES ON DATABASE wownder TO wownder;

export FLASK_APP=wsgi.py

```




## TODO:
 - Complete this TODO with instruction to run this project.
 - Complete this TODO with real task.


import os
import logging
log = logging.RootLogger(logging.INFO)
import redis
from operator import itemgetter
import time
import pytz
from datetime import datetime
from operator import itemgetter
from eventmanager import services


os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'
import django
django.setup()
import requests
from graphqlendpoint.models import Agent
if os.getenv("MODE"):
    MODE = os.environ['MODE']

if MODE == 'OMNITRACKER':

    b = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=5)
    log.info("Connected to Redis, Database 2, port 6379")
    if os.getenv("OMNITRACKER_API_ENABLED") == "True":
        log.warning('ENABLED OMNITRACKER API enabled on this host')

    while True:
        for key in b.keys('*'):
            try:
                c = b.hgetall(key)
            except redis.exceptions.ResponseError:
                pass
            s = services.Services(c)
            if s.done == True:
                b.delete(key)

if MODE == 'FRONTEND':
    os.environ['OMNITRACKER_API_ENABLED'] = 'FALSE'
    log.warning('FRONDEND MODE')
    f = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)
    b = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=5)
    log.info("Connected to Redis, Database 2, port 6379")

    while True:
        keys = f.keys('*')
        for key in keys:
            try:
                c = f.hgetall(key)
            except redis.exceptions.ResponseError:
                pass
            s = services.Services(c)
            if s.done == True:
                backendkeys = b.keys('*')
                while backendkeys > 5:
                    # we let the backend catch up
                    time.sleep(0.1)
                    backendkeys = b.keys('*')
                b.hmset(key, c)
                f.delete(key)

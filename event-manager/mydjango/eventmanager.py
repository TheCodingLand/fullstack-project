
import logging
log = logging.RootLogger(logging.INFO)
import redis
from operator import itemgetter
import time
import pytz
from datetime import datetime
from operator import itemgetter
from eventmanager import services

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'
import django
django.setup()
import requests
from graphqlendpoint.models import Agent
if os.environ
r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)
log.info("Connected to Redis, Database 2, port 6379")
if os.getenv("OMNITRACKER_API_ENABLED") == "True":
    log.error('ENABLED OMNITRACKER API!!!!')


def getAddedCalls():
    for key in r.keys('*'):
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        s = services.Services(c)
        if s.done == True:
            r.delete(key)


while True:
    getAddedCalls()

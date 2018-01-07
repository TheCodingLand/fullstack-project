import os
import logging

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


b = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)
logging.warning("Connected to Redis, Database 2, port 6379")


while True:
    for key in b.keys('*'):
        try:
            c = b.hgetall(key)
        except redis.exceptions.ResponseError:
            logging.error('Faild to deal with key %s' % key)
            b.delete(key)
            continue
        s = services.Services(c)
        if s.done == True:
            b.delete(key)

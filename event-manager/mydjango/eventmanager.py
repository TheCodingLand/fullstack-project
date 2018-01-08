import os
import logging
import redis
from eventmanager import services

from graphqlendpoint.models import Agent, Event, Call, Transfer, Ticket, Category

cats=Category.ojects.all()
for cat in cats:
    cat.delete()

os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'
import django
django.setup()

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

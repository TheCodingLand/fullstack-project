import os
import logging
import redis
from eventmanager import services
import time
import django
from eventmanager import ot_api
from datetime import timedelta, datetime



os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'

django.setup()

b = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)
logging.warning("Connected to Redis, Database 2, port 6379")
ot=ot_api.ot_api_event()
ot.updateTickets()
batch = datetime.now()
d = timedelta(minutes=15)

while True:

    if batch - d > datetime.now():
        ot.updateTickets()
        batch = datetime.now()



    keys = b.keys('*')
    if len(keys) == 0:
        #easier on CPU usage
        time.sleep(0.1)
    for key in keys:

        try:
            c = b.hgetall(key)
        except redis.exceptions.ResponseError:
            logging.error('Faild to deal with key %s' % key)
            b.delete(key)
            continue
        s = services.Services(c)
        if s.done == True:
            b.delete(key)

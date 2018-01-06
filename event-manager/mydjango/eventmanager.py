
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


''' users = []
url = 'http://ot-ws:5000/api/ot/objects/'
payload = {
    "objectclass": "Agent",
    "filter": "",
    "variables":
    []}

req = requests.post(url, payload)

print(requests)

agents = Agent.objects.all()

for item in req:
    log("%s" % item) '''


r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)

log.warning("CLEANUP MODE ENABLED")
try:
    k = r.keys()
    for i in k:
        i.delete()


log.info("Connected to Redis, Database 2, port 6379")


def getAddedCalls():
    for key in r.scan_iter(match='*'):
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        s = services.Services(c)
        if s.done == True:
            r.delete(key)

# quick cleaup as this key is only used for real time data


log.info("Waiting for startup of other components, so we can clear redis db all at once")
time.sleep(10)
log.info("Backlog Clearing Started")


keyhashes = []
keys = r.keys()

for key in keys:
    try:
        k = r.hgetall(key)
        k['key'] = key
        keyhashes.append(k)
    except:
        key.delete()

orderedlist = sorted(keyhashes, key=itemgetter('timestamp'))
log.info(len(orderedlist))
for item in orderedlist:

    s = services.Services(item)
    if s.done == True:
        r.delete(item['key'])


log.info("Normal Loop")
while True:

    getAddedCalls()

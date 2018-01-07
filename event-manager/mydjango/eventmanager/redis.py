import redis
import json

pub = redis.StrictRedis(host="redis", port=6379, db=3)

from graphqlendpoint.models import Agent, Event, Call, Transfer
if os.getenv("MODE"):
    MODE = os.environ['MODE']


class Redis(object):
    def __ini__(self):
        pass

    def update(self, item, id, data):
        if MODE == 'OMNITRACKER':
            return
        pub.publish('agent', 'app changed changed %s - %s' % (item, id))
        # push new state data to redis for frontend subscription

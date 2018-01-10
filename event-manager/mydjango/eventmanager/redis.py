import redis
import json
import os
pub = redis.StrictRedis(host="redis", port=6379, db=3)

from graphqlendpoint.models import Agent, Event, Call, Transfer


class Redis(object):
    def __ini__(self):
        pass

    def update(self, item, id, data):
        pub.publish('agent', '{ item : "%s", id: "%s", data: "%s" }' % (item, id, data))
        # push new state data to redis for frontend subscription

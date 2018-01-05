import redis
import json

pub = redis.StrictRedis(host="redis", port=6379, db=3)
#dataconn = redis.StrictRedis(host="redis", port=6379, db=4)
from graphqlendpoint.models import Agent, Event, Call, Transfer

class Redis(object):
    def __ini__(self):
        pass
    def update(self, item, id , data):
        #notify server that the data has been updated for the frontend

        pub.publish('agent', id)
        #push new state data to redis for frontend subscription
        #d = { 'id': id }
        #js = json.dumps(d)
        #dataconn.lpush('agent', js)
        
    
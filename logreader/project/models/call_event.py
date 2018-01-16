import json
import redis
conn = redis.StrictRedis(host="redis", port=6379, db=2)
import logging

class CallEvent(object):

    def __init__(self, id, date):
        self.id = id
        self.timestamp = date

    def add(self):
        hash = "%s-%s-%s" % (self.timestamp, 'create', self.id)
        """storing a add call into redis"""
        data = {'action': 'create',
                'timestamp': "%s" % self.timestamp, 'id': self.id}
        conn.hmset(hash, data)

    def newCentraleCall(self, ext):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'centrale', ext, self.id)
        data = {'action': 'centrale',
                'timestamp': "%s" % self.timestamp, 'id': self.id, 'data': ext}
        conn.hmset(hash, data)

    def setCaller(self, phone):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'setcaller', phone, self.id)
        data = {'action': 'setcaller', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': phone}
        conn.hmset(hash, data)

    def setDetails(self, calltype):
        hash = "%s-%s-%s-%s" % (self.timestamp,
                                'setdetails', calltype, self.id)
        data = {'action': 'setdetails', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': calltype}
        conn.hmset(hash, data)

    def transfer(self, ext):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'transfer', ext, self.id)
        data = {'action': 'transfer',
                'timestamp': "%s" % self.timestamp, 'id': self.id, 'data': ext}
        conn.hmset(hash, data)

    def consult(self, ext):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'consult', ext, self.id)
        data = {'action': 'consult', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': ext}
        conn.hmset(hash, data)

    def end(self):
        hash = "%s-%s-%s" % (self.timestamp, 'remove', self.id)
        data = {'action': 'remove',
                'timestamp': "%s" % self.timestamp, 'id': self.id}
        conn.hmset(hash, data)

    def retrieved(self, ext):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'retrieved', self.id, ext)
        data = {'action': 'retrieved',
                'timestamp': "%s" % self.timestamp, 'id': self.id, 'data': ext}
        logging.error("RETRIEVING ext %s" % self.getRetrieving())
        conn.hmset(hash, data)

    def consulting(self, ext):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'consulting', self.id, ext)
        data = {'action': 'consulting',
                'timestamp': "%s" % self.timestamp, 'id': self.id, 'data': ext}
        conn.hmset(hash, data)

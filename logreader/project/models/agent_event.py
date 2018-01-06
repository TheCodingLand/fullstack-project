import json
import redis
conn = redis.StrictRedis(host="redis", port=6379, db=2)


class AgentEvent(object):

    def __init__(self, id, date):

        self.id = id
        self.timestamp = date

    def linkCall(self, ucid):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'linkcall', self.id, ucid)
        data = {'action': 'linkcall', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (ucid)}
        conn.hmset(hash, data)

    def changeacdState(self, state):
        hash = "%s-%s-%s-%s" % (self.timestamp,
                                'changeACDstate', self.id, state)
        data = {'action': 'changeACDstate', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (state)}
        conn.hmset(hash, data)

    def changedevState(self, state):
        hash = "%s-%s-%s-%s" % (self.timestamp,
                                'changeDeviceState', self.id, state)
        data = {'action': 'changeDeviceState', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (state)}
        conn.hmset(hash, data)

    def login(self, state):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'login', self.id, state)
        data = {'action': 'login', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (state)}
        conn.hmset(hash, data)

    def logoff(self, state):
        hash = "%s-%s-%s-%s" % (self.timestamp, 'logoff', self.id, state)
        # print(hash)
        data = {'action': 'logoff', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (state)}
        conn.hmset(hash, data)

    def update_agent_ext(self, state):
        hash = "%s-%s-%s-%s" % (self.timestamp,
                                'update_agent_ext', self.id, state)
        data = {'action': 'update_agent_ext', 'timestamp': "%s" % self.timestamp,
                'id': self.id, 'data': '%s' % (state)}
        conn.hmset(hash, data)

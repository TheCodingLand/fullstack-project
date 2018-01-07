import pytz
import os

from eventmanager.dispatch_services import dispatch

from datetime import datetime
paris = pytz.timezone('Europe/Paris')


class Services(object):
    """class that determines which what to do with which redis key"""

    def __init__(self, redishash):
        self.done = False
        self.redishash = redishash
        datestr = self.redishash.get('timestamp')
        self.id = redishash.get('id')
        if not self.id:
            print("not a key to manage")
            return True
        self.action = redishash.get('action')
        self.data = ""
        if redishash.get('data'):
            self.data = redishash.get('data')
        try:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f')
        except:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        self.timestamp = paris.localize(dt)

        # CALLS
        if self.action == "create":
            self.done = dispatch().create_call(self.id, self.timestamp)
        if self.action == "centrale":
            self.done = dispatch().centrale(self.id, self.timestamp, self.data)
        if self.action == "transfer":
            self.done = dispatch().transfer_call(
                self.id, self.timestamp, self.data)
        if self.action == "setdetails":
            self.done = dispatch().update_details(
                self.id, self.timestamp, self.data)
        if self.action == "setcaller":
            self.done = dispatch().set_caller(
                self.id, self.timestamp, self.data)
        if self.action == "remove":
            self.done = dispatch().end(self.id, self.timestamp)

        # AGENTS
        if self.action == "login":
            self.done = dispatch().login(self.id, self.data)
        if self.action == "update_agent_ext":
            self.done = dispatch().update_agent_ext(self.id, self.data)

        if self.action == "changeACDstate":
            self.done = dispatch().changeACDstate(self.id, self.data)
        if self.action == "linkcall":
            self.done = dispatch().linkcall(self.id, self.data)
        if self.action == "changeDeviceState":
            self.done = dispatch().changeDeviceState(self.id, self.data)
        if self.action == "logoff":
            self.done = django = dispatch().logoff(self.id, self.data)
        if self.done == False:
            print("KEY kept in queue : %s : %s, %s" %
                  (self.id, self.action, self.data))

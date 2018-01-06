import pytz

from eventmanager.dispatch_services import django_calls_services, django_agents_services
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
            self.done = django_calls_services().create_call(self.id, self.timestamp)
        if self.action == "centrale":
            self.done = django_calls_services().centrale(self.id, self.timestamp)
        if self.action == "transfer":
            self.done = django_calls_services().transfer_call(
                self.id, self.timestamp, self.data)
        if self.action == "setdetails":
            self.done = django_calls_services().update_details(
                self.id, self.timestamp, self.data)
        if self.action == "setcaller":
            self.done = django_calls_services().set_caller(
                self.id, self.timestamp, self.data)
        if self.action == "remove":
            self.done = django_calls_services().end(self.id, self.timestamp)

        # AGENTS
        if self.action == "login":
            self.done = django_agents_services().login(self.id, self.data)

        if self.action == "changeACDstate":
            self.done = django_agents_services().changeACDstate(self.id, self.data)
        if self.action == "linkcall":
            self.done = django_agents_services().linkcall(self.id, self.data)
        if self.action == "changeDeviceState":
            self.done = django_agents_services().changeDeviceState(self.id, self.data)
        if self.action == "logoff":
            self.done = django = django_agents_services().logoff(self.id, self.data)
        if self.done == False:
            print("KEY kept in queue : %s : %s, %s" %
                  (self.id, self.action, self.data))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
import json
from graphqlendpoint.models import Agent, Event, Call, Transfer
import requests
from django.db import connection
from eventmanager.redis import Redis


class django_calls_services(object):
    def __init__(self):
        # there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()

    def centrale(self, id, timestamp, ext):
        centrale = Agents.objects.get_or_create(ext=ext)
        centrale.isQueueLine = True
        centrale.firstname = "Centrale IVR"
        centrale.ot_userloginname = "Centrale"
        centrale.save()

    def create_call(self, id, timestamp):
        redis = Redis().update('agent', id, "createcall")
        call = Call.objects.get_or_create(ucid=id)[0]
        call.start = timestamp
        call.save()
        return True

    def set_caller(self, id, timestamp, data):
        redis = Redis().update('agent', id, data)
        call = Call.objects.get_or_create(ucid=id)[0]
        call.origin = data
        call.save()

        return True

    def update_details(self, id, timestamp, data):
        redis = Redis().update('agent', id, data)
        call = Call.objects.get_or_create(ucid=id)[0]
        call.call_type = data
        call.save()

        return True

    def ot_create_event(self, call):

        if "OMNITRACKER_API_URL_ENABLED" in os.environ:
            if os.environ[OMNITRACKER_API_URL_ENABLED] == "TRUE":
                url = 'http://ot-ws:5000/api/ot/events/events/ucid/%s' % call.ucid
                if call.event:
                    if call.event.ot_id:
                        url = 'http://ot-ws:5000/api/ot/events/events/%s' % call.event.ot_id

                resp = requests.get(url=url)
                ot = json.loads(resp.text)
                #print (ot)

                if resp.status_code == 404:
                    #print ("create event in ot as is doesnt exist")
                    event = Event(creationdate=call.start)
                    event.call = call
                    event.save()

                print("getting id")
                ot = json.loads(resp.text)
                print(ot.get('id'))

                if hasattr(call, 'event'):
                    call.event.ot_id = ot.get('id')
                    call.save()

                elif resp.status_code == 200:
                    if ot['id'] != 0:
                        #print (ot['id'])
                        event = Event.objects.get_or_create(ot_id=ot['id'])[0]
                        event.save()
                        call.event = event

                        if hasattr(call, 'event'):
                            call.event.ot_id = ot['id']
                            call.save()

    def transfer_call(self, id, timestamp, destination):
        #print("managing a transfer")
        redis = Redis().update('agent', id, destination)
        call = Call.objects.get_or_create(ucid=id)[0]

        agent = Agents.objects.get(ext=destination)
        if agent.isQueueLine:
            call.isContactCenterCall = True
            call.save()
            self.ot_create_event(call)
            # we probably missed this extension as a queue line

        transfers = call.getTransfers().filter(
            ttimestamp=timestamp, tdestination=destination)
        # check if this exists already
        if len(transfers) > 0:
            return True
        else:
            call = Call.objects.update_or_create(ucid=id)[0]
            if call.destination == "":
                origin = ""
            else:
                origin = call.destination

        agents = Agent.objects.filter(ext=destination)

        if len(agents) == 1:
            agent = agents[0]
            agent.current_call = None
            agent.save()
            agent.current_call = call

            if origin != destination:
                t = Transfer(call=call, torigin=origin,
                             tdestination=destination, ttimestamp=timestamp)
                t.save()
            call.updatehistory()
            call.destination = destination
            call.save()
            agent.save()
        return True

    def end(self, id, timestamp):
        redis = Redis().update('agent', id, "endcall")
        call = Call.objects.update_or_create(ucid=id)[0]
        call.end = timestamp
        call.state = "ended"

        agents = Agent.objects.filter(current_call=call)

        if len(agents) > 0:
            for agent in agents:
                agent.current_call = None
                agent.save()

        call.save()

        return True

    def update_agent(self):

        return True


class django_agents_services(object):

    def __init__(self):
        connection.close()

    def login(self, id, data):
        redis = Redis().update('agent', id, data)
        self.agent = Agent.objects.get_or_create(phone_login=id)[0]
        self.agent.phone_active = True

        #

        if data != "False":

            if data != self.agent.ext:
                # We need to remove the extention from the old login
                agent_old = Agent.objects.filter(ext=data)

                if len(agent_old) == 1:
                    if agent_old[0] != self.agent:
                        agent_old[0].ext = agent_old[0].phone_login
                        agent_old[0].phone_state = False
                        agent_old[0].save()

            else:
                self.agent.ext = data
        self.agent.save()

        return True

    def changeACDstate(self, id, data):
        redis = Redis().update('agent', id, data)
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.phone_state = data
            self.agent.save()

        except:
            pass

        return True

    def linkcall(self, id, data):
        #print ("linkCall agent : %s, call %s" % (id, data))

        redis = Redis().update('agent', id, data)
        return True

    def changeDeviceState(self, id, data):
        redis = Redis().update('agent', id, data)
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.device_state = data
            self.agent.save()

        except:
            pass

        return True

    def logoff(self, id, data):
        redis = Redis().update('agent', id, data)
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.phone_active = False
            self.agent.save()

        except:
            pass

        return True

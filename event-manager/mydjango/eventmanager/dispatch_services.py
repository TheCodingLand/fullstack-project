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
from eventmanager.ot_api import ot_api_event

import logging
log = logging.Logger("dispatcher")
log.setLevel(logging.WARNING)


class dispatch(object):

    def __init__(self):
        # there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()

    # calls

    def centrale(self, id, timestamp, ext):
        log.info("Call in IVR,%s" % ext)
        call = Call.objects.get_or_create(ucid=id)[0]
        call.start = timestamp
        call.destination = ext
        call.isContactCenterCall = True
        call.save()

        centrale = Agent.objects.get_or_create(ext=ext)[0]
        centrale.isQueueLine = True
        centrale.firstname = "Centrale IVR"
        centrale.ot_userloginname = "Centrale"
        centrale.current_call = None
        centrale.save()
        centrale.call = call
        centrale.save()

        return ot_api_event().create(call)

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
        ot_api_event().updateEventPhoneNumber(call)
        return True

    def update_details(self, id, timestamp, data):
        redis = Redis().update('agent', id, data)
        call = Call.objects.get_or_create(ucid=id)[0]
        call.call_type = data
        call.save()
        ot_api_event().updateEventType(call)
        return True

    def transfer_call(self, id, timestamp, destination):
        #print("managing a transfer")
        redis = Redis().update('agent', id, destination)
        call = Call.objects.get_or_create(ucid=id)[0]

        agents = Agent.objects.filter(ext=destination)
        if len(agents) > 0:
            if agents[0].isQueueLine:
                if call.isContactCenterCall == False:
                    self.centrale(id, timestamp, destination)

        transfers = call.getTransfers().filter(
            ttimestamp=timestamp, tdestination=destination)
        # check if this exists already
        if len(transfers) == 0:
            torigin = call.destination
            if torigin != destination:
                t = Transfer(call=call, torigin=torigin,
                             tdestination=destination, ttimestamp=timestamp)
                t.save()
            call.updatehistory()
            call.destination = destination
            call.save()

            if len(agents) == 1:
                agent = agents[0]
                agent.current_call = None
                agent.save()
                agent.current_call = call
                agent.save()
                ot_api_event().transfer(call, agent)

                # ot_api_event().transfer(call)
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
        # ot_api_event().updateEndDate(call)
        return True

    def update_agent_ext(self, id, data):
        agent = Agent.objects.get_or_create(phone_login=id)[0]
        if agent.ext == data:
            return True
        else:
            agents_old = Agent.objects.filter(ext=data)
            if len(agents_old) > 0:
                for a_old in agents_old:
                    a_old.ext = a_old.phone_login
                    a_old.phone_active = False
                    a_old.save()

            agent.ext = data
            agent.save()

        return True

    # agents
    def login(self, id, data):
        log.info("agent login received,%s" % id)
        redis = Redis().update('agent', id, data)
        agent = Agent.objects.get_or_create(phone_login=id)[0]
        agent.phone_active = True

        #

        if data != "False":

            if data != agent.ext:
                # We need to remove the extention from the old login
                agent_old = Agent.objects.filter(ext=data)

                if len(agent_old) == 1:
                    if agent_old[0] != agent:
                        agent_old[0].ext = agent_old[0].phone_login
                        agent_old[0].phone_state = False
                        agent_old[0].save()

                agent.ext = data
        agent.save()

        return True

    def changeACDstate(self, id, data):
        log.info("agent state change received,%s : %s" % (id, data))
        redis = Redis().update('agent', id, data)
        try:
            agent = Agent.objects.get(phone_login=id)
            agent.phone_state = data
            agent.save()

        except:
            pass

        return True

    def linkcall(self, id, data):
        #print ("linkCall agent : %s, call %s" % (id, data))

        redis = Redis().update('agent', id, data)
        return True

    def changeDeviceState(self, id, data):
        log.info("device state change received,%s : %s" % (id, data))
        redis = Redis().update('agent', id, data)
        try:
            agent = Agent.objects.get(phone_login=id)
            agent.device_state = data
            agent.save()

        except:
            pass

        return True

    def logoff(self, id, data):
        log.info("agent logoff received,%s" % id)
        redis = Redis().update('agent', id, data)
        try:
            agent = Agent.objects.get(phone_login=id)
            agent.phone_active = False
            agent.save()

        except:
            pass

        return True

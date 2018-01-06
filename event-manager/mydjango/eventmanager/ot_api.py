import os
import requests
from graphqlendpoint.models import Agent, Event, Call, Transfer
import logging
log = logging.Logger("EventToOTService")
log.setLevel(logging.INFO)


class ot_api_event(object):
    def __init__(self):
        self.url = 'http://ot-ws:5000/api/ot/'

    def get_ot_id_from_call(self, id):
        event = Events.object.get(call=call)
        return event.ot_id

    def get_ot_id_from_ucid(self, ucid):
        """Temporary as we have two systems injecting events"""
        payload = {
            "objectclass": "Event",
            "filter": "EventUCID",
            "variables":
            [{
                "name": "UCID",
                        "value": "%s" % ucid
            }]}
        req = requests.post(url, payload)
        try:
            id = req.get('id')
        except KeyError:
            log.error("Could not create Event with payload %s" % payload)
            return False
        return id

    def create(self, call):

        id = self.get_ot_id_from_ucid(call.ucid)
        if id:
            log.info("event already in the system, skipping creation")
            event = Events.object.get_or_create(ot_id=id)
            event.save()

        payload = {"UCID": call.ucid,
                   "Applicant": "Centrale", "Responsible": "Centale", "Source": "Call Incoming"}
        url = "%s/events" % self.url
        req = requests.post(url, payload)
        try:
            id = req.get('id')
        except KeyError:
            log.error("Could not create Event with payload %s" % payload)
            return False
        url = "%s/%s" % (url, id)
        payload = {"CreationDate": call.start}
        req = requests.post(url, payload)

        event = Events.objects.get_or_create(ot_id=id)
        event.call = call
        event.save()

        # good to have the same date for the event as the start of the call

    def updateApplicant(self, call, agent):
        payload = {"Applicant": agent.ot_userdisplayname}
        url = "%s/events/%s" % (self.url, id)

        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            event = Events.object.get()
            log.info("updated applicant to %s" % agent.ot_userdisplayname)
            return True

    def updateResponsible(self, call, agent):
        payload = {"Responsible": agent.ot_userdisplayname}
        url = "%s/events/%s" % (self.url, objecttype, id)
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.info("updated responsible to %s" % agent.ot_userdisplayname)
            return True

    def updateEndDate(self, call):
        payload = {"Call Finished Date": call.end}
        url = "%s/events/%s" % (self.url, id)

        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.info("updated end date to %s" % agent.ot_userdisplayname)
            return True

    def updateEventPhoneNumber(self, call):
        payload = {"Phone Number": call.origin}
        url = "%s/events/%s" % (self.url, objecttype, id)

        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.info("updated event phone number to %s" % call.origin)
            return True

    def updateEventHistory(self, call):
        payload = {"TransferHistory": call.history}
        url = "%s/events/%s" % (self.url, id)

        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.info("updated event history to %s" % call.history)
            return True

    def updateEventType(self, call):
        payload = {"Title": call.call_type}
        url = "%s/events/%s" % (self.url, id)
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.info("updated event history to %s" % call.call_type)
            return True

    def transfer(self, call):
        return True

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
        # log.error(ucid)
        payload = '{ "objectclass": "Event", "filter": "EventUCID", "variables": [ { "name": "UCID", "value": "%s" } ], "requiredfields": [] }' % ucid

        log.error(payload)
        url = 'http://ot-ws:5000/api/ot/objects'
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        log.error(req.text)
        try:
            data = req.json()
            id = data['Event'][0]['id']
        except KeyError:
            log.error("Could not get Event with payload %s" % payload)
            return False
        return id

    def create(self, call):

        id = self.get_ot_id_from_ucid(call.ucid)
        if id:
            log.error("event already in the system, skipping creation")
            event = Events.object.get_or_create(ot_id=id)
            event.save()

        payload = '{ "UCID": call.ucid, "Applicant": "Centrale", "Responsible": "Centale", "Source": "Call Incoming" }'
        url = "%s/events" % self.url
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        try:
            id = req.get('id')
        except KeyError:
            log.error("Could not create Event with payload %s" % payload)
            return False
        url = "%s/%s" % (url, id)
        payload = {"CreationDate": call.start}
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})

        event = Events.objects.get_or_create(ot_id=id)
        event.call = call
        log.error("updated call to %s" % event.ot_id)
        event.save()

        # good to have the same date for the event as the start of the call

    def updateApplicant(self, call, agent):
        payload = '{"Applicant": "%s"}' % agent.ot_userdisplayname
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            event = Events.object.get()
            log.error("updated applicant to %s" % agent.ot_userdisplayname)
            return True

    def updateResponsible(self, call, agent):
        payload = '{"Responsible": "%s"}' % agent.ot_userdisplayname
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.error("updated responsible to %s" % agent.ot_userdisplayname)
            return True

    def updateEndDate(self, call):
        payload = '{"Call Finished Date": "%s"}' % call.end
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})

        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.error("updated end date to %s" % agent.ot_userdisplayname)
            return True

    def updateEventPhoneNumber(self, call):
        payload = '{"Phone Number": "%s"}' % call.origin
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.error("updated event phone number to %s" % call.origin)
            return True

    def updateEventHistory(self, call):
        payload = '{"TransferHistory": "%s"}' % call.history
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.error("updated event history to %s" % call.history)
            return True

    def updateEventType(self, call):
        payload = '{"Title": "%s"}' % call.call_type
        url = "%s/events/%s" % (self.url, id)
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        if req.status_code == 404:
            return False
        elif req.status_code == 200:
            log.error("updated event history to %s" % call.call_type)
            return True

    def transfer(self, call, agent):
        self.checkUserStatus(agent)

        if agent.ot_userdisplayname != "":
            payload = '{"Applicant": "%s", "Responsible" : "%s", "TransferHistory": "%s"}' % (
                call.history, agent.displayname)
            url = "%s/events/%s" % (self.url, id)
            req = requests.post(url, payload, headers={
                                "Content-Type": "application/json"})
            if req.status_code == 404:
                return False
            elif req.status_code == 200:
                log.error("updated event history to %s" % call.call_type)
                return True
            return False

    def checkUserStatus(self, agent):

        url = '%s/objects' % self.url
        payload = '{ "objectclass": "Agent", "filter": "agentfromext", "variables": [{ "name": "Phone", "value": "-%s"}], "requiredfields": [] }' % agent.ext
        req = requests.post(url, payload, headers={
                            "Content-Type": "application/json"})
        data = req.json()
        agent.ot_userdisplayname = data['Agent']['Title']
        if data['status'] == "success":
            for item in data['Agent'][0]:
                agent.ot_id = item['id']
                agent.firstname = item['data']['FirstName']
                agent.lastname = item['data']['LastName']
                agent.ot_userloginname = item['data']['Login Name']
                agent.ot_userdisplayname = item['data']['Title']
                agent.email = item['data']['Email Address']
                agent.save()

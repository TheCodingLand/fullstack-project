import os
import requests
from graphqlendpoint.models import Agent, Event, Call, Transfer
import logging
log = logging.Logger("EventToOTService")
log.setLevel(logging.INFO)
import json
ENABLED = False
if os.getenv("OMNITRACKER_API_ENABLED") == "TRUE":
    ENABLED = True


class ot_api_event(object):
    def __init__(self):
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
        self.url = 'http://ot-ws:5000/api/ot/'

    def get_ot_id_from_call(self, id):
        event = Event.objects.get(call=call)
        return event.ot_id

    def execute(self, method, url, payload):

        if ENABLED:
            if method not in ['get', 'post', 'put']:
                log.error('invalid method %s' % method)
                return False
            if method == 'post':
                req = requests.post(url, json=payload, headers=self.headers)
            if method == 'put':
                req = requests.put(url, json=payload, headers=self.headers)
            if method == 'get':
                req = requests.get(url, json=payload, headers=self.headers)

            if req.status_code == 201:
                log.info(req.status_code)
                return req
            elif req.status_code == 200:
                log.info(req.status_code)
                return req
            if req.status_code == 404:
                log.info(req.status_code)
                return False
            if req.status_code == 400:
                log.error("ERROR : 400 !! method :%s, url:%s, payload:%s" % (
                    method, url, json.dumps(payload)))
                return False
            if req.status_code == 500:
                log.error("ERROR : 500 !! method :%s, url:%s, payload:%s" % (
                    method, url, payload))
                return False
            else:
                log.error("UNKNOWN API ERROR !! method :%s, url:%s, payload:%s" % (
                    method, url, payload))
                log.error('api error !')
                return False

        else:
            log.info('API DISABLED')
            return False

    def get_ot_id_from_ucid(self, ucid):
        """Temporary as we have two systems injecting events"""
        # log.error(ucid)
        payload = {"objectclass": "Event", "filter": "EventUCID", "variables": [
            {"name": "UCID", "value": "%s" % ucid}], "requiredfields": []}
        id = 0
        # log.error(payload)
        url = 'http://ot-ws:5000/api/ot/objects'
        req = self.execute('post', url, payload)
        if req == False:
            return False
        try:
            data = req.json()
            id = data['Event'][0]['id']
        except:
            log.error("Could not get Event with payload %s" %
                      json.dumps(payload))
            return False
        return id

    def put(self, ucid):
        payload = {'UCID': '%s' %
                   ucid, 'Applicant': 'Centrale', 'Source': 'Call Incoming'}
        url = 'http://ot-ws:5000/api/ot/events'
        req = self.execute('put', url, payload)

        if req == False:
            return False

        data = req.json()

        try:
            id = data['event']
        except KeyError:
            log.error("Could not create Event with payload %s" %
                      json.dumps(payload))
            return False
        return id

    def create(self, call):

        id = self.get_ot_id_from_ucid(call.ucid)
        if id:
            event = Event.objects.get_or_create(ot_id=id)[0]
            event.save()

        else:
            id = self.put(call.ucid)
            url = 'http://ot-ws:5000/api/ot/event/%s' % (id)
            payload = {"CreationDate": "%s" % call.start}
            req = self.execute('put', url, payload)
        if id:
            event = Event.objects.get_or_create(ot_id=id)[0]
            event.call = call
            #log.error("updated call to %s" % event.ot_id)
            event.save()
        return True

        # good to have the same date for the event as the start of the call

    def updateApplicant(self, call, agent):
        payload = {"Applicant": "%s" % agent.ot_userdisplayname}
        url = '%s/events/%s' % (self.url, id)
        req = self.execute('put', url, payload)
        if req == False:
            return False
        else:
            log.info("updated applicant to %s" % agent.ot_userdisplayname)
            return True

    def updateResponsible(self, call, agent):
        payload = {"Responsible": "%s" % agent.ot_userdisplayname}
        url = '%s/event/%s' % (self.url, id)
        req = self.execute('put', url, payload)
        if req == False:
            return False
        else:
            log.info("updated responsible to %s" % agent.ot_userdisplayname)
            return True

    def updateEndDate(self, call):
        payload = {"Call Finished Date": "%s" % call.end}
        url = '%s/event/%s' % (self.url, id)
        req = self.execute('put', url, payload)

        if req == False:
            return False
        else:
            log.error("updated end date to %s" % agent.ot_userdisplayname)
            return True

    def updateEventPhoneNumber(self, call):
        payload = {"Phone Number": "%s" % call.origin}
        url = '%s/event/%s' % (self.url, id)
        req = self.execute('put', url, payload)
        if req == False:
            return False
        else:
            log.error("updated event phone number to %s" % call.origin)
            return True

    def updateEventHistory(self, call):
        payload = {"TransferHistory": "%s" % call.history}
        url = '%s/event/%s' % (self.url, id)
        req = self.execute('put', url, payload)
        if req == False:
            return False
        else:
            log.error("updated event history to %s" % call.history)
            return True

    def updateEventType(self, call):
        payload = {"Title": "%s" % call.call_type}
        url = '%s/events/%s' % (self.url, id)
        req = self.execute('put', url, payload)
        if req == False:
            return False
        else:
            log.error("updated event type to %s" % call.call_type)
            return True

    def transfer(self, call, agent):

        self.checkUserStatus(agent)

        if agent.ot_userdisplayname != "":
            if agent.isQueueLine == False:

                payload = {"Applicant": "%s" % agent.ot_userdisplayname,
                           "TransferHistory": "%s" % call.history}
            else:
                payload = {"Applicant": "Centrale",
                           "TransferHistory": "%s" % call.history}

            url = '%s/event/%s' % (self.url, id)
            req = self.execute('put', url, payload)
            if req == False:
                return False
            else:
                log.error("updated event history to %s" % call.call_type)
                return True
            return False

    def checkUserStatus(self, agent):

        if agent.ot_userdisplayname == None:
            log.error("user not defined, getting data from Web service")
            url = 'http://ot-ws:5000/api/ot/objects'
            payload = {"objectclass": "Agent", "filter": "userbyext", "variables": [
                {"name": "Phone", "value": "-%s" % agent.ext}], "requiredfields": []}
            req = self.execute('post', url, payload)

            if req == False:
                log.error("FAILED ! %s")
                return False
            else:
                data = req.json()
                if data['status'] == "success":
                    for item in data['Agent'][0]:
                        agent.ot_id = item['id']
                        agent.firstname = item['data']['FirstName']
                        agent.lastname = item['data']['LastName']
                        agent.ot_userloginname = item['data']['Login Name']
                        agent.ot_userdisplayname = item['data']['Title']
                        agent.email = item['data']['Email Address']
                        agent.save()

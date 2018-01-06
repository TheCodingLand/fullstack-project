import os
import requests


class ot_api_event(object):
    def __init__(self):
        self.url = 'http://ot-ws:5000/api/ot/'

    def get_ot_id_from_call(id):
        event = Events.object.get(call=call)
        return event.ot_id

    def create_event(self, callobj):

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
        event.call = callobj
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

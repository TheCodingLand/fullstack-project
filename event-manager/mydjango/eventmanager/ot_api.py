import os
import requests
from graphqlendpoint.models import Agent, Event, Call, Transfer, Ticket, Category
from django.core.exceptions import ObjectDoesNotExist
import datetime
import logging
log = logging.Logger("EventToOTService")
log.setLevel(logging.INFO)
import json
ENABLED = False
headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
if os.getenv("OMNITRACKER_API_ENABLED") == "TRUE":
    ENABLED = True

def execute(method, url, payload):
    if ENABLED:
        if method == 'post':
            req = requests.post(url, json=payload,headers=headers)
        if method == 'put':
            req = requests.put(url, json=payload,headers=headers)
            if req.status_code >201:
                log.error("modification OT : %s, %s --------- > %s : %s" % (payload, req.text, req.status_code, url))
        if method == 'get':
            req = requests.get(url, headers=headers)


        if req.status_code == 201:
            log.info(req.status_code)
            return req
        if req.status_code == 200:
            log.info(req.status_code)
            return req
        if req.status_code== 301:
            log.info(req.status_code)
            return req
        if req.status_code == 404:
            if "Call Finished Date" in payload.keys():
                log.error("%s not found %s, %s" % (req.status_code, url, req.text))
            return False
        if req.status_code == 400:
            log.error("ERROR : 400 !! method :%s, url:%s, payload:%s, %s" % (
                method, url, json.dumps(payload), req.text))
            return False
        if req.status_code == 500:
            log.error("ERROR : 500 !! method :%s, url:%s, payload:%s" % (
                method, url, payload))
            return False
        else:
            log.error("UNKNOWN API ERROR !! method :%s, url :%s, payload:%s" % (
                method, url, payload))
            log.error('api error %s!' % req.text)
            return False

    else:
        log.error('API DISABLED')
        return False

class ot_api_event(object):
    def __init__(self):

        self.url = 'http://ot-ws:5000/api/ot/'

    def get_ot_id_from_call(self, call):
        try:
            event = Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return None
        return event.ot_id

    def execute(self, method, url, payload):
        if ENABLED:
            if method == 'post':
                req = requests.post(url, json=payload,headers=self.headers)
            if method == 'put':
                req = requests.put(url, json=payload,headers=self.headers)
            if method == 'get':
                req = requests.get(url, headers=self.headers)

            if req.status_code == 201:
                log.info(req.status_code)
                return req
            if req.status_code == 200:
                log.info(req.status_code)
                return req
            if req.status_code== 301:
                log.info(req.status_code)
                return req
            if req.status_code == 404:
                if "Call Finished Date" in payload.keys():
                    log.error("%s not found %s, %s" % (req.status_code, url, req.text))
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
                log.error("UNKNOWN API ERROR !! method :%s, url :%s, payload:%s" % (
                    method, url, payload))
                log.error('api error %s!' % req.text)
                return False

        else:
            log.error('API DISABLED')
            return False





    def get_ot_id_from_ucid(self, ucid):
        """Temporary as we have two systems injecting events"""
        # log.error(ucid)
        payload = {"objectclass": "Event", "filter": "EventUCID", "variables": [
            {"name": "UCID", "value": "%s" % ucid}], "requiredfields": []}
        id = 0
        # log.error(payload)
        url = 'http://ot-ws:5000/api/ot/objects'
        req = execute('post', url, payload)
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


        req = execute('put', url, payload)

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
            req = execute('put', url, payload)
        if id:
            event = Event.objects.get_or_create(ot_id=id)[0]
            event.call = call
            #log.error("updated call to %s" % event.ot_id)
            event.save()
        return True

        # good to have the same date for the event as the start of the call

    def updateApplicant(self, call, agent):
        try:
            event = Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return False
        payload = {"Applicant": "%s" % agent.ot_userdisplayname}
        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        req = execute('put', url, payload)
        event.applicant=agent
        event.save()
        if req == False:
            return False
        else:
            log.info("updated applicant to %s" % agent.ot_userdisplayname)
            return True






    def updateResponsible(self, call, agent):
        try:
            event = Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return False
        payload = {"Responsible": "%s" % agent.ot_userdisplayname}

        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        req = execute('put', url, payload)
        event.responsible = agent
        event.save()
        if req == False:
            return False
        else:
            log.info("updated responsible to %s" % agent.ot_userdisplayname)
            return True



    def updateEndDate(self, call):
        try:
            event = Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return False

        if event.ot_id is None:
            log.error("no OT ID in event !!")
            return False

        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        payload = {"Call Finished Date": "%s" % call.end}

        #req = execute('get', url, payload)

        req = execute('put', url, payload)
        event.end = call.end
        event.save()
        if req == False:
            log.error("couldn't do the updates ! ")
            return False
        #updating event and tickets
        ot_api_event().getTicketFromEvent(call)

    def updateEventPhoneNumber(self, call):

        events = Event.objects.filter(call=call)
        if len(events) > 0:
            event = events[0]
        else:
            log.error("event not found !! %s" % call.ucid)
            return False

        payload = {"Phone Number": "%s" % call.origin}
        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        req = execute('put', url, payload)
        event.phone=call.origin
        event.save()
        if req == False:
            return False
        else:
            log.error("updated event phone number to %s" % call.origin)
            return True





    def updateEventHistory(self, call):
        try:
            event = Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return False


        payload = {"TransferHistory": "%s" % call.history}
        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        req = execute('put', url, payload)
        event.transferhistory = call.history
        event.save()
        if req == False:
            return False
        else:
            log.error("updated event history to %s" % call.history)
            return True

    def updateEventType(self, call):
        events = Event.objects.filter(call=call)
        if len(events) > 0:
            event = events[0]
        else:
            log.error("event not found !! %s" % call.ucid)
            return False

        payload = {"Title": "%s" % call.call_type}
        url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id
        req = execute('put', url, payload)


        if req == False:
            return False
        else:
            log.error("updated event type to %s" % call.call_type)
            return True

    def transfer(self, call, agent):
        if agent.isQueueLine == False:
            self.checkUserStatus(agent)
        events = Event.objects.filter(call=call)
        if len(events) >0:
            event=events[0]
        else:
            log.error("event not found !! %s" % call.ucid)
            return False

        if agent.ot_userdisplayname != "" and event.ot_id != None:
            if agent.isQueueLine == False:
                #log.error("updating event with applicant %s" % agent.ot_userdisplayname)

                payload = {"Applicant": "%s" % agent.ot_userdisplayname,
                           "TransferHistory": "%s" % call.history}
            else:
                payload = {"Applicant": "Centrale",
                           "TransferHistory": "%s" % call.history}

            url = 'http://ot-ws:5000/api/ot/event/%s' % event.ot_id

            req = execute('put', url, payload)
            event.applicant = agent
            event.save()
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
            req = execute('post', url, payload)

            if req == False:
                log.error("FAILED ! %s")
                return False
            else:
                data = req.json()
                if data['status'] == "success":
                    for item in data['Agent']:
                        agent.ot_id = item['id']
                        agent.firstname = item['data']['FirstName']
                        agent.lastname = item['data']['LastName']
                        agent.ot_userloginname = item['data']['Login Name']
                        agent.ot_userdisplayname = item['data']['Title']
                        agent.email = item['data']['Email Address']
                        agent.save()

    def getTicketFromEvent(self, call):
        try:
            event=Event.objects.get(call=call)
        except ObjectDoesNotExist:
            return

        if event.ot_id == None:
            return False
        req = execute(
            'get', 'http://ot-ws:5000/api/ot/events/%s' % event.ot_id, "")
        if req == False:
            return False
        data = req.json()
        try:
            agent=Agent.objects.get(ot_id=data['data']['Applicant'])
            event.Applicant= agent

        except ObjectDoesNotExist:
            pass

        event.phone=data['data']['Phone Number']
        event.end =data['data']['Call Finished Date']
        ticket_id = data['data']['RelatedIncident']
        if ticket_id =="":
            return False
        #log.error("Ticket id : %s" % ticket_id)
        ticket = Ticket.objects.get_or_create(ot_id=ticket_id)[0]
        event.ticket = ticket
        event.save()

        requiredfields= { 'requiredfields': ['CreationDate', 'Title', 'SolutionDescription', 'AssociatedCategory' , 'Applicant',  'Responsible', 'State'] }

        req = execute('post', 'http://ot-ws:5000/api/ot/object/%s' % ticket_id, requiredfields)

        data = req.json()
        #log.error(data)
        ticket.title = data['data']['Title']
        ticket.creationdate = data['data']['CreationDate']
        ticket.category = self.getCategory(data['data']['AssociatedCategory'])
        try:
            ticket.applicant =Agent.objects.get(ot_userdisplayname=data['data']['Applicant'])

        except ObjectDoesNotExist:
            ticket.applicant = None

        try :
            ticket.responsible =Agent.objects.get(ot_userdisplayname=data['data']['Responsible'])
        except ObjectDoesNotExist:
            ticket.applicant = None

        ticket.applicant = ticket.applicant
        ticket.responsible = ticket.responsible
        ticket.state = data['data']['State']
        ticket.solution = data['data']['SolutionDescription']
        ticket.save()


    def getCategory(self, id):

        cat = Category.objects.get_or_create(ot_id=id)[0]
        if cat.title==None:
            req = execute('get', 'http://ot-ws:5000/api/ot/ot_objects/%s' % id, '')
            if req==False:
                log.error(req)
                return None
            data = req.json()
            #log.error(data)
            cat.title = data['data']['Title']
            cat.seachcode= data['data']['SearchCode']
            cat.predecessor= data['data']['Predecessor']
            cat.save()
        return cat


    def updateTickets(self):
        d = datetime.timedelta(days=1)
        calls = Call.objects.filter(start__gt= datetime.datetime.today()-d)
        for call in calls:
            self.getTicketFromEvent(call)


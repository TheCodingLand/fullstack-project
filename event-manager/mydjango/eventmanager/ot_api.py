import os
import requests
''' class Category(models.Model):
    title = models.CharField(max_length=200, null=True)
    predecessor = models.IntegerField(null=True, blank=True)
    searchcode = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)

    

creationdate = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True, blank=True)
    ot_id = models.IntegerField(null=True, blank=True)
    applicant = models.ForeignKey(
        Agent, related_name='events_applicant', on_delete=models.CASCADE, null=True, blank=True)
    responsible = models.ForeignKey(
        Agent, related_name='events_responsible', on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    transferhistory = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    ticket = models.ForeignKey(
        Ticket, related_name='tickets', on_delete=models.CASCADE, null=True, blank=True)
    call = models.ForeignKey(
        Call, on_delete=models.SET_NULL, null=True, related_name='event', blank=True)

 '''


class ot_api(object):
    def __init__(self):
        self.url = 'http://ot-ws:5000/api/ot/'

    def get_event_by_ot_id(self, objectName, id):
        self.url = "%s/%s/id/%s" % (self.url, objectName, id)
        resp = requests.get(url=url)
        ot = json.loads(resp.text)
        log.info(resp.text)
        if resp.status_code == 404:
            return False

        elif resp.status_code == 200:
            ot = json.loads(resp.text)
            log.info(ot.get('id'))
            if ot['id'] != 0:
                event = Event.objects.get_or_create(ot_id=ot['id'])[0]
                event.save()
            return event
        return False

    def create(self, objectName, callObject):

        payload = {"UCID": "12312323",
                   "Applicant": "Centrale", "Responsible": "Centale"}

        self.url = "%s/events" % self.url
        resp = requests.post(url, payload)
        try:
            resp.get('id')
        except KeyError:
            log.error("Could not create Event with payload %s" % payload)

        {
            "UCID": "string",
            "CreationDate": "2018-01-06T15:37:11.961Z",
            "Call Finished Date": "2018-01-06T15:37:11.961Z",
            "Applicant": "login name from an agent",
            "Responsible": "login name from an agent",
            "State": "a state",
            "RelatedIncident": 0
        }
        self.url = "%s/%s/event/%s" % (self.url, objectName, id)
        resp = requests.get(url=url)

        event = Event.objects.get_or_create(ot_id=ot['id'])[0]
        self.get(event, call)
        event = Event.objets.get(call=callObject)

        self.url = "%s/%s/id/%s" % (self.url, objectName, id)
        resp = requests.get(url=url)

        origin = models.CharField(max_length=200, null=True)
        destination = models.CharField(max_length=200, null=True)
        call_type = models.CharField(max_length=200, null=True)
        start = models.DateTimeField(max_length=200, null=True)
        end = models.DateTimeField(max_length=200, null=True, blank=True)
        isContactCenterCall = models.BooleanField(default=False)
        history = models.CharField(max_length=600, null=True)
        call.
        self.get(objectName, )
        'http://ot-ws:5000/api/ot/events/events/ucid/%s' % call.ucid

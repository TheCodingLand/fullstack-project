import os
import requests

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


class ot_api(object):
    def __init__(self):
        self.url = 'http://ot-ws:5000/api/ot/'

    def get(self, objectName, id):
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
            return ot['id']
        return False



    def update(self, objectName, **kwargs):
        self.get(objectName, )
        'http://ot-ws:5000/api/ot/events/events/ucid/%s' % call.ucid

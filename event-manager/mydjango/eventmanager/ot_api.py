import os
import requests
class ot_api(object):
    def __init__(self):
        self.url = 'http://ot-ws:5000/api/ot/'


    def get(self, objectName, id):
        self.url = "%s/%s/id/%s" % (self.url,objectName,id)
         resp = requests.get(url=url)
                ot= json.loads(resp.text)
                #print (ot)
                
                if resp.status_code==404:
                    #print ("create event in ot as is doesnt exist")
                    event = Event(creationdate = call.start)
                    event.call = call
                    event.save()


                print ("getting id")
                ot=json.loads(resp.text)
                print (ot.get('id'))
                
                if hasattr(call, 'event'):
                    call.event.ot_id = ot.get('id')
                    call.save()
                
                elif resp.status_code==200:
                    if ot['id'] !=0:
                        #print (ot['id'])
                        event =Event.objects.get_or_create(ot_id=ot['id'])[0]
                        event.save()
                        call.event = event

                        if hasattr(call, 'event'):
                            call.event.ot_id = ot['id']
                            call.save()

    def create(self, objectName, **kwargs):
        'http://ot-ws:5000/api/ot/events/events/ucid/%s' % call.ucid
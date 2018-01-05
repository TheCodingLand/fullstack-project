import pytz

from eventmanager.django_services import django_calls_services, django_agents_services

from datetime import datetime

paris=pytz.timezone('Europe/Paris')



class Services(object):
    """class that determines which what to do with which redis key"""
    def __init__(self, redishash):
        
        
        self.redishash=redishash
        datestr = self.redishash.get('timestamp')

        self.id = redishash.get('id')
        #if not self.id:
        #    print ("not a key to manage")
        #    return True
        self.action = redishash.get('action')
        self.done=False
        self.data = ""
        if redishash.get('data'):
            self.data = redishash.get('data')
        try:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f')
        except:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        
        self.timestamp = paris.localize(dt)
        
        #CALLS
        
        if self.action == "create":
            self.done = self.onCallCreate()
            
        if self.action == "transfer":
            self.done = self.onCallTransfer()
        if self.action == "setdetails":
            self.done = self.onCallDetails()
        if self.action == "setcaller":
            self.done = self.onCallerUpdated()
        if self.action == "changestate":
            self.done = self.onAgentChangeState()
        if self.action == "remove":
            self.done = self.onCallFinished()
        
        #AGENTS  
        if self.action == "login":
            self.done = self.login()
        if self.action == "changeACDstate":
            self.done = self.changeACDstate()
        if self.action == "linkcall":
            self.done = self.linkcall()
        if self.action == "changeDeviceState":
            self.done = self.changeDeviceState()
        if self.action == "logoff":
            self.done = self.logoff()
        
        if self.done==False:
            print("KEY kept in queue : %s : %s, %s" % (self.id,self.action,self.data))
    
    # CALLS
    def onCallCreate(self):
        django = django_calls_services().create_call(self.id, self.timestamp)

        return django
        
    def onCallTransfer(self):
        django = django_calls_services().transfer_call(self.id, self.timestamp,self.data)
        #
        return django
    
    def onCallDetails(self):
        django = django_calls_services().update_details(self.id, self.timestamp, self.data)
        #ot = ot_services.update_details(id)        
    
        return django

    def onCallerUpdated(self):
        django = django_calls_services().set_caller(self.id, self.timestamp, self.data)
        #ot = ot_services.update_details(id)        
      
       
        return django

    def onCallFinished(self):
        django= django_calls_services().end(self.id, self.timestamp)
        #ot=ot_services.end(id)
           
        return django
    
    #AGENTS
    
    def login(self):
        django = django_agents_services().login(self.id, self.data)
        
        
        return django
    
    def logoff(self):
        django = django_agents_services().logoff(self.id, self.data)
       
        return django
        
    def linkcall(self):
        django = django_agents_services().linkcall(self.id, self.data)
      
        return django
        
    def changeDeviceState(self):
        django = django_agents_services().changeDeviceState(self.id, self.data)
  
        return django
    def changeACDstate(self):
        django = django_agents_services().changeACDstate(self.id, self.data)
 
        return django
        
        


from graphqlendpoint.models import Agent, Call, Event

class eventparser(object):
    def __init__(self, json):
        super(Event, self).__init__(json)
        """Lets be stric with ot objects management"""
        try:
            self.event = Call.objects.get(ucid=id)
        except:
            self.event=False
        
        if ot_Event:
            for key, value in json:
                if key == "Applicant":
                    agent=Agent.objects.get_or_create(ot_userdisplayname=value)
                    event.applicant=agent             
                if key == "Call Finished Date":
                    event.end= value
                if key == "CreationDate":
                    event.creationdate= value
                if key == "Phone Number":
                    event.phone=value
                if key == "RelatedIncident":
                    event.ticketid=value
                if key == "Responsible":
                    pass
                if key == "TransferHistory":
                    pass
        
    def updateApplicant(self):
        if self.
    
class ticketparser(object):
    def __init__(self, json):
        event = ot_Ticket()
        self.json = json
        for key, value in json:
            if key == "Applicant":
                pass
            if key == "Description":
                pass
            if key == "CreationDate":
                pass
            if key == "Title":
                pass
            if key == "RelatedIncident":
                pass
            if key == "Responsible":
                pass
            if key == "SolutionDescription":
                pass
            if key == "AssociatedCategory":
                pass
            if key == "State":
                pass
                
                
class agentparser(object):
    def __init__(self, json):
        agent = ot_Agent()
        self.json = json
        for key, value in json:
            if key == "FirstName":
                
                pass
            if key == "Description":
                pass
            if key == "CreationDate":
                pass
            if key == "Title":
                pass
            if key == "RelatedIncident":
                pass
            if key == "Responsible":
                pass
            if key == "SolutionDescription":
                pass
            if key == "AssociatedCategory":
                pass
            if key == "State":
                pass
                
                                
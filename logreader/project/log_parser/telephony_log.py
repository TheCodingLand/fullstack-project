from project.models.call_event import CallEvent
from project.log_parser.log_line import LogLine


class TelephonyLog(LogLine):
    def __init__(self, line):
        super(TelephonyLog, self).__init__(line)

    def parse(self):
        self.check_createNew()
        self.getDetails()
        self.getTransfers()
        self.manageEnd()
        
    def check_createNew(self):
        if self.getNewCallUcid():
            CallEvent(self.getNewCallUcid(), self.date).add()
    
    def getDetails(self):
        if "UpdateRoutingData" in self.line:
            ev = CallEvent(self.getUcid(),self.date)
            ev.setDetails(self.getCallType())
    
    def getTransfers(self):
        if self.getEstablished() and self.getUcid():
            calling = self.getCalling()
            ev=CallEvent(self.getUcid(),self.date)
            ev.setCaller(calling)
            destination = self.getAnswerExt()
            ev = CallEvent(self.getUcid(),self.date)
            ev.transfer(self.getAnswerExt())
            
            
            
            
    def manageEnd(self):
        if self.getTerminated():
            ev = CallEvent(self.getUcid(),self.date)
            ev.end()
    


    def getUcid(self):
        return self.search(r"UCID<(.*?)>")

    def getCalling(self):
        return self.search(r"CallingDID:([0-9]+)\(S\)")
    
    def getAnswerExt(self):
        return self.search(r"AnswerDID:(.*?)\(S\)")
    
    def getDestination(self):
        return self.search(r"DestinationDID:(.*?)\(S\)")

    def getNewCallUcid(self):
        return (self.search(r"New Call object with UCID: (.*?)\s"))

    def getCallType(self):
        return self.search(r", CallTypeName:(.*?),")

    def getDiverted(self):
        return "Diverted Event," in self.line
        
    def getTransferred(self):
        return "Transferred Event," in self.line

    def getEstablished(self):
        return "Established Event," in self.line
        
    def getTerminated(self):
        return "Remove UCID<" in self.line

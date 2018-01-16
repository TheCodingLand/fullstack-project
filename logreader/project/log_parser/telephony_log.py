from project.models.call_event import CallEvent
from project.log_parser.log_line import LogLine
import logging

class TelephonyLog(LogLine):
    def __init__(self, line):
        super(TelephonyLog, self).__init__(line)

    def parse(self):
        self.check_createNew()
        self.isCentrale()
        self.getDetails()
        self.getTransfers()
        self.manageEnd()
        self.manageRetrieved()
        self.manageConsulting()

    def manageConsulting(self):
        if self.consulting():
            ev = CallEvent(self.getUcid(), self.date)
            ev.setDetails(self.consulting(self.getCalledDid()))

    def check_createNew(self):
        if self.getNewCallUcid():
            CallEvent(self.getNewCallUcid(), self.date).add()

    def getDetails(self):
        if "UpdateRoutingData" in self.line:
            ev = CallEvent(self.getUcid(), self.date)
            ev.setDetails(self.getCallType())

    def getTransfers(self):
        if self.getEstablished() and self.getUcid():
            calling = self.getCalling()
            ev = CallEvent(self.getUcid(), self.date)
            ev.setCaller(calling)
            destination = self.getAnswerExt()
            ev = CallEvent(self.getUcid(), self.date)
            ev.transfer(self.getAnswerExt())

    def manageEnd(self):
        if self.getTerminated():
            ev = CallEvent(self.getUcid(), self.date)
            ev.end()

    def isCentrale(self):
        if "DivertDestination" in self.line and "DIVERT_IVR_DISTRIBUTION" in self.line:
            ev = CallEvent(self.getUcid(), self.date)
            ev.newCentraleCall(self.getCentaleNumber())

    def manageRetrieved(self):
        if self.getRetrieved():
            ev = CallEvent(self.getUcid(), self.date)
            logging.error("RETRIEVING ext %s" % self.getRetrieving())
            ev.retrieved(self.getRetreiving())

    def getSubjectDID(self):
        return self.search(r"SubjectDID: (.*?)\(S\)")

    def getCalledDid(self):
        return self.search(r"CalledDID: (.*?)\(S\)")

    def getRetreiving(self):
        return self.search(r"RetrievingDID:(.*?)\(S\)")

    def getCentaleNumber(self):
        return self.search(r"DivertDestination: (.*?),")

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

    def getRetrieved(self):
        return "Retrieved Event, UCID <" in self.line

    def consulting(self):
        return ", LCS: Connected, Cause: Consultation, Trunk:" in self.line


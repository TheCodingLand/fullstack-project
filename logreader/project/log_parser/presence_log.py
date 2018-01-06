from project.models.agent_event import AgentEvent
from project.log_parser.log_line import LogLine


class PresenceLog(LogLine):
    def __init__(self, line):
        super(PresenceLog, self).__init__(line)

    def parse(self):
        if self.getUserId():
            self.linkedCall()
            self.changeACDState()
            self.changeDeviceState()
            self.login()
            self.logoff()
            self.check_agent_ext()

    def check_agent_ext(self):
        if self.getUserId() and self.getExtension():
            if len(self.getExtension == 3) and len(self.getUserId == 3):
                AgentEvent(self.getUserId(), self.date).update_agent_ext(
                    self.getExtension())

    def login(self):
        if self.isLoginIn():
            AgentEvent(self.getUserId(), self.date).login(self.getExtension())

    def logoff(self):
        if self.isLoginOff():
            AgentEvent(self.getUserId(), self.date).logoff(self.getExtension())

    def linkedCall(self):
        if self.getUcid():
            AgentEvent(self.getUserId(), self.date).linkCall(self.getUcid())

    def changeACDState(self):
        if self.getAcdState():
            AgentEvent(self.getUserId(), self.date).changeacdState(
                self.getAcdState())
        if self.getUnavailable():
            AgentEvent(self.getUserId(), self.date).changeacdState(
                'ACDUNAVAIL')
        if self.getAvailable():
            AgentEvent(self.getUserId(), self.date).changeacdState('ACDAVAIL')

    def changeDeviceState(self):
        if self.getLineState():
            AgentEvent(self.getUserId(), self.date).changedevState(
                self.getLineState())

    def getUserId(self):
        return self.search(r"UserId\{(.*?)\}")

    def getExtension(self):
        return self.search(r"Extension\{(.*?)\}")

    def getAcdState(self):
        state = self.search(r"Acd State\{(.*?)\}")
        if state == False:
            state = self.search(
                r"TpsSUserPresence::OnEvent. Rcvd Agent (ACDAVAIL)")
        return state

    def getUnavailable(self):
        state = r"TpsSUserPresence::OnEvent. Rcvd Agent ACDUNAVAIL Event for UserId{" in self.line or "TpsSUserPresence::OnEvent. Rcvd Agent ACDUNAVAIL Event for UserId{" in self.line
        return state

    def getAvailable(self):
        state = r"TpsSUserPresence::OnEvent. Rcvd Agent ACDAVAIL Event for UserId{" in self.line or "TpsSUserPresence::OnEvent. Rcvd Agent ACDAVAIL Event for UserId{" in self.line

        return state

    def getLineState(self):
        return self.search(r"State\{(.*?)\}\}\]\}")

    def getUcid(self):
        return self.search(r"HandlingState:\{ContactId/RqC\{(.*?)\/")

    def isLoginIn(self):
        if "TpsSUserPresence::OnEvent. Rcvd Client Logon Event" in self.line:
            return True
        elif "Cause{Desktop Logon}" in self.line:
            return True
        elif "Cause{Media Logon},Extension{" in self.line:
            return True
        return False

    def isLoginOff(self):
        if "SActiveAgent::Logoff." in self.line:
            return True
        elif "TpsSUserPresence::OnEvent. Rcvd Client Logoff" in self.line:
            return True
        elif "Cause{Media Logoff},Extension{" in self.line:
            return True
        return False
# 1b70 TpsSUserPresence::SendEvent. UserMediaStateEvent:{ChangedMedia{Voice},UserId{107},Cause{Media Logon},Extension{534},MediaState:{Media{Voice},State{Logon},Cause{None},StartTime{2018/01/02 06:32:08.853}},Routing State:{State{Unavailable},Reason{0},Source{CTI Query}},Presence State:{Active},Presence State(ExDC):{Away},Affected Contact:{HandlingState{ContactId/RqC{4781514871127062/-1},State{Busy}}}}

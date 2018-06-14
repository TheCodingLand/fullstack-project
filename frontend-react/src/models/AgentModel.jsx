import { observable, action } from "mobx";




export default class AgentModel {

  @observable phoneLogin;
  @observable firstname;
  @observable lastname;
  @observable phoneState;
  @observable currentCall;
  @observable totalcalls;
  @observable callsWithoutTickets;
  @observable otUserdisplayname;
  constructor(agent, rootstore) {
    console.log("Loading New Agent")
    //console.log"Agent Constructor")
    this.ds = rootstore.ds;
    
    
    this.firstname = agent.firstname;
    this.lastname = agent.lastname;
    this.phoneLogin = agent.phoneLogin;
    this.ext = agent.ext;
    this.phoneState = agent.phoneState;
    this.totalcalls = "";
    this.currentCall = { }
    this.totalcalls = []
    this.getCallsCount() 
    this.callsWithoutTickets = []
    this.currentUser = false
    this.otUserdisplayname = agent.otUserdisplayname
    if (rootstore.currentUser.ext === this.ext) {
    this.getCallsWithoutTickets()
    this.currentUser=true
    this.socket={}
  
    }
    
  }

  @action
  setCurrentUser() {
 
    this.currentUser = true
  }

  @action
  updateState(state) {
  
    this.phoneState = state;
    
  }

  @action
  removeCall() {
    this.currentCall = {}

    this.getCallsCount()
  }

  getCallsCount(){
  this.ds.getCallsbyAgentExt(this.ext).then((data) => { this.totalcalls= data.data.allCalls.edges.length })
}



  onCallsWithoutTicketsRecieved(data) {
    this.totalcalls = data.data.allCalls.edges.length
    let events = []
    events = data.data.allCalls.edges.reduce((filtered, data) => {
      if (data.node.event.edges[0]) {
        if (data.node.event.edges[0].node.otId) {
          if (!data.node.event.edges[0].node.ticket) {
            const d = new Date(data.node.start)
            let event = { 'id': data.node.ucid, 'start': d.toString(), 'origin': data.node.origin, 'otId': data.node.event.edges[0].node.otId }
            filtered.push(event)
          }
        }
      }
      return filtered
    },[])
    this.callsWithoutTickets = events
  }

  updateTickets(socket) {
    this.socket=socket
    this.ds.getEventsbyAgentExt(this.ext).then((data) => { this.onCallsWithoutTicketsRecievedUpdate(data) })
  }

  onCallsWithoutTicketsRecievedUpdate(data) {
    
    
    data.data.allCalls.edges.forEach((data) => {
      if (data.node.event.edges[0]) {
        if (data.node.event.edges[0].node.otId)
        {
          this.socket.send("updatetickets:"+data.node.event.edges[0].node.otId)
        }
      
    
    }
    
  })

}

  
  getCallsWithoutTickets() {
    
    console.log(`updating events without tickets for phone number ${this.ext}`)
    this.ds.getEventsbyAgentExt(this.ext).then((data) => { this.onCallsWithoutTicketsRecieved(data) })
  }


  @action
  setCall(call) {
    console.log("SetCall" + call.ucid + " " + call.destination + " " + call.origin )
    this.currentCall = call

    this.ds.getTicketbyPhone(call.origin).then((data) => this.onTicketsRecieved(data))
    
   
    
    this.getCallsWithoutTickets()
    

  }


  onTicketsRecieved(data) {
    
    this.currentCall.tickets = data.data.allEvents.edges.reduce((filtered,edge) => {
      if (edge.node.ticket) {
         filtered.push(edge.node.ticket)
      }
      return filtered}
    ,[])

 
  }

  @action
  updateCall(call) {
      this.setCall(call)
    }


  

  
  onCallRecieved(data) {
    console.log("onCallRecieved")


    let listofcalls = [];
    if (data.data.allCalls) { listofcalls = data.data.allCalls.edges.map((edge) => { return edge.node }) }

    if (listofcalls.length > 0) {

      this.setCall(listofcalls[0])

    }
  }
}
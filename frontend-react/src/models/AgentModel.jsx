import { observable, action } from "mobx";
import DataProvider from './../DataProvider'



export default class AgentModel {
  
  @observable phoneLogin;
  @observable firstname;
  @observable lastname;
  @observable phoneState;
  @observable phoneState;
  @observable currentCall;

  constructor(agent) {
    
    this.ds = new DataProvider();  

    this.firstname = agent.firstname;
    this.lastname = agent.lastname;
    this.phoneLogin = agent.phoneLogin;
    this.ext = agent.ext;
    this.phoneState = agent.phoneState;
  
    this.currentCall = { ucid : "", origin : "", start : "", destination : "", callType : "", tickets: [] }
    
    if (agent.currentCall) {
      if (agent.currentCall.ucid) {
      
      this.currentCall = { ucid : agent.currentCall.ucid, origin : agent.currentCall.origin, start : agent.currentCall.start, destination : agent.currentCall.destination, callType: agent.currentCall.callType, tickets : []}
      this.ds.getTicketbyPhone(agent.currentCall.origin).then((data) => this.onTicketsRecieved(data))
  } 
}
  }

  @action
  updateState(state) {
    this.phoneState = state;
  }

  @action
  removeCall()
  {
    this.currentCall.ucid=""
    this.currentCall.origin = ""
    this.currentCall.start = ""
    this.currentCall.destination = ""
    this.currentCall.callType =""
    this.currentCall.tickets= null
    
  }
  
  @action
  setCall(call){
  
    this.currentCall.ucid = call.ucid
    
    this.currentCall.start = call.start
    this.currentCall.destination = call.destination
    this.currentCall.callType = call.callType
    if (call.origin !== "False") {
      this.currentCall.origin = call.origin
      this.ds.getTicketbyPhone(call.origin).then((data) => this.onTicketsRecieved(data))
    }
    else{
      this.currentCall.origin = "hidden"
    }
    

    //this.currentCall = call;
    
  }
  
  @action
  onTicketsRecieved(data){
    this.currentCall.tickets = data.data.allEvents.edges.map((edge) =>  { 
      
      if (edge.node.ticket){
        console.log(edge)
        console.log(edge.node.ticket.title)
        
      return edge.node.ticket}
    else {
      return ""
    }
  }
    )
      
    

    
  }

  @action
  updateCall(ucid) {
    this.ds.GetCall(ucid).then((data) => this.onCallRecieved(data))
    
 
   }

  @action
  ticketByPhone(phonenumber) {

  }

  onCallRecieved(data) {
    
    let listofcalls = [];
    if (data.data.allCalls) { listofcalls = data.data.allCalls.edges.map((edge) => { return edge.node })}
    
    if (listofcalls.length >0) {
     
      this.setCall(listofcalls[0])

      

  }
  
}
 
 
    
  }
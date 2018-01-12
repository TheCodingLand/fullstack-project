import { observable, extendObservable, action } from "mobx";
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
    this.currentCall = agent.currentCall;
    
  }

  @action
  updateState(state) {
    this.phoneState = state;
  }

  @action
  removeCall()
  {
    this.currentCall = {}
  }
  
  @action
  setCall(call){
    this.currentCall=call
    console.log(call)
  }

  @action
  updateCall(ucid) {
    this.ds.GetCall(ucid).then((data) => this.onCallRecieved(data))
  }

  onCallRecieved(data) {
    let currentCall= {}
    let listofcalls = [];
    if (data.data.allCalls) { listofcalls = data.data.allCalls.edges.map((edge) => { return edge.node })}
    if (listofcalls.length ==1) {
       currentCall = { 
        ucid : listofcalls[0].ucid,
        origin : listofcalls[0].origin,
        start : listofcalls[0].start,
        call_type : listofcalls[0].callType,
        destination : listofcalls[0].destination
      
    }
  }
  this.setCall(currentCall)
}
 
 
    
  }
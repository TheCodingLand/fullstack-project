import { observable, computed, action } from "mobx";
import AgentModel from "./AgentModel";

//actions:
//calls : newcall, phonenumber, calltype, transfer, endcall
//agents : login, logoff, changestate, linkcall

export default class AgentListModel {
  constructor(rootStore) {
    
      this.rootStore = rootStore
    }
    
//    this.GetAgentList()
 @observable queues = [];
 @observable incomingCalls= [];
 @observable agents = [];

 handleMessage(data){
      
        if (data.action==="logoff") {      
          for (let i = 0; i < this.agents.length; i++) {
            if (data.id === this.agents[i].phoneLogin) {
              
              this.removeAgent(this.agents[i])
            }
          }
        }
        if (data.action==="login") {
         
          this.GetAgent(data.id)}
        
        if (data.action==="changestate") {
         
          for (let i = 0; i < this.agents.length; i++) {
            if (data.id === this.agents[i].phoneLogin) {
              this.agents[i].updateState(data.data)  
          
            }
          }
        }
        if (data.action==="transfer") {
          this.GetQueuesUpdates()
          for (let i = 0; i < this.agents.length; i++) {
            if (data.data === this.agents[i].phoneLogin) {
              this.agents[i].updateCall(data.id)
            }
          }
        }
        if (data.action==="endcall") {
          this.GetQueuesUpdates()
          for (let i = 0; i < this.agents.length; i++) {
            if (data.data === this.agents[i].phoneLogin) {
            
              this.agents[i].removeCall()
              
            }
          }
        }
        if (data.action === "create" ) {
          this.GetQueuesUpdates()
          console.log("updating queue")
        }
        if (data.action === "calltype" ) {
          this.GetQueuesUpdates()
          console.log("updating queue")
        }
       
      
      }
    

  @computed
  get loggedInAgentsCount() {
    return this.agents.filter(agent => agent.state).length;
  }

  @action
  removeAgent(agent){
  this.agents.remove(agent)
}

 

  @action
  addAgent(agent) {
    //console.log(agent)
    this.agents.push(new AgentModel(agent))
  }

  @action
  async GetAgentList() {
    
    //this.ds.ListAgents().then((data) => console.log(data))    
    this.rootStore.ds.ListAgents().then((data) => this.onListRecieved(data))
  }

  @action
  async GetQueuesUpdates(){
  this.rootStore.ds.getQueueLines().then((data) => this.onQueuesRecieved(data))
  }

  onListRecieved(data) {
    var listofusers = [];
    if (data.data.allAgents) { listofusers = data.data.allAgents.edges.map((edge) => { return edge.node })}
    this.agents = []
    listofusers.map((user) => this.addAgent(user))
    //this.setState( { serverData : { users : users.users } }
  }

  

  onQueuesRecieved(data) {
    var listofqueues = [];
    if (data.data.allAgents) { listofqueues = data.data.allAgents.edges.map((edge) => { return edge.node })}
    this.queues = []
    listofqueues.map((queue) => this.addQueue(queue))
  //this.setState( { serverData : { users : users.users } }
 }

 @action
 addQueue(queue) {
   //console.log(agent)
   this.queues.push(new AgentModel(queue))
 }


  @action
  async GetAgent(login) {
    //this.ds.ListAgents().then((data) => console.log(data))    
    this.rootStore.ds.GetAgent(login).then((data) => this.onAgentRecieved(data))

  }

  onAgentRecieved(data) {
    var listofusers = [];
    if (data.data.allAgents) { listofusers = data.data.allAgents.edges.map((edge) => { return edge.node })}
    //var users = { users : listofusers }
    if (listofusers.length ===1)
    {
    let found = false;
    for (let i = 0; i < this.agents.length; i++) {
      if (listofusers[0].phoneLogin === this.agents[i].phoneLogin) {
        let agent= new AgentModel(listofusers[0])
        this.agents[i] = agent
        found = true;
      }
      if (found === false) {
        this.addAgent(new AgentModel(listofusers[0]))
      }
    }
   }
    //this.setState( { serverData : { users : users.users } }
  }

}

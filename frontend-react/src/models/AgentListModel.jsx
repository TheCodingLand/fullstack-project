import { observable, computed, action } from "mobx";
import AgentModel from "./AgentModel";
import CallModel from "./CallsModel";

//actions:
//calls : newcall, phonenumber, calltype, transfer, endcall
//agents : login, logoff, changestate, linkcall

export default class AgentListModel {
  constructor(ds, socket) {
    this.ds = ds
    this.socket=socket
  }

  @observable calls = []
  @observable queues = []
  @observable agents = []

  currentUser = { }

  async handleMessage(data) {
    if (data.action === "logoff") {
      console.log(`logoff detected for ${data.id}`)
      for (let i = 0; i < this.agents.length; i++) {
        if (data.id === this.agents[i].phoneLogin) {
          this.removeAgent(this.agents[i])
        }
      }
    }

    if (data.action === "login") {
      console.log(`login detected for ${data.id}`)
      this.GetAgent(data.id)
    }

    if (data.action === "changestate") {
      console.log(`State change detected for ${data.id}, into ${data.data}`)
      for (let i = 0; i < this.agents.length; i++) {
        if (data.id === this.agents[i].phoneLogin) {
          this.agents[i].updateState(data.data)
        }
      }
    }

    if (data.action === "transfer") {
      this.getActiveCalls()
      
      console.log(`transfer detected for ${data.data}, call : ${data.id}`)

      this.queues.forEach((queue) => {
        if (queue.currentCall.ucid === data.id) {
          queue.currentCall = {}
        }
      })
      this.agents.forEach((agent) => {
        if (agent.currentCall.ucid === data.id) {
          agent.currentCall = {}
        }
      }
    )

      this.agents.forEach(agent => { if (agent.login === data.data) {
        this.calls.forEach(call => { if (call.ucid === data.id) { 

          console.log("transfering call " + data.id)
          call.destination = agent.ext 
          agent.updateCall(call)

        } })
          
      }
    }
    )
    }

    /* if (data.action === "transferring") {
      for (let i = 0; i < this.agents.length; i++) {
        if (data.data === this.agents[i].phoneLogin) {
          this.GetAgent(data.data)
          data.
        }
      }
    } */

    if (data.action === "endcall") {

      console.log(`call end detected for ${data.data}, call : ${data.id}`)
      this.calls.forEach(call => { if (call.ucid === data.id) { 
        console.log("removing call " + data.id)
        this.calls.remove(call) } })
      for (let i = 0; i < this.queues.length; i++) {
        if (this.queues[i].currentCall) {
          if (data.id === this.queues[i].currentCall.ucid) {
            this.queues[i].currentCall= {}
          }
        }
      }
      
      for (let i = 0; i < this.agents.length; i++) {
        if (data.data === this.agents[i].phoneLogin) {
          this.agents[i].currentCall= {}
          this.agents[i].updateState(data.data)
        
      }
    }
  
    }

    if (data.action === "create") {
      console.log(`detected create call ${data.id}`)
      this.getActiveCalls()
      
    }
    if (data.action === "calltype") {
      this.calls.forEach(call => { if (call.ucid === data.id) { this.setCallType(call, data.data)}})
    }
  }
  
  @action
  setCallType(call, calltype) {
    call.callType = calltype
  }


  @computed
  get loggedInAgentsCount() {
    return this.agents.filter(agent => agent.state).length;
  }

  @action
  removeAgent(agent) {
    this.agents.remove(agent)
  }

  @action
  setCurrentUser(agent) {
    console.log(`current user SET ! : ${agent.ext}`)
    
    agent.getCallsWithoutTickets()
    this.currentUser=agent
    agent.currentUser=true
    agent.updateTickets(this.socket)
    
  }

  @action
  addAgent(agent) {
    this.agents.push(new AgentModel(agent, this))
  }

  getActiveCalls(){
    this.ds.getActiveCalls().then((calls) => {calls.data.allCalls.edges.map(call => { return this.updateCalls(call) } ) })
    //.then(      calls => this.onCallsRecieved(calls)) 
  }
  
  @action
  updateQueue(call){
    this.queues.forEach((queue) => { 
    
      if (call.destination === queue.ext) {
      queue.currentCall = call

    }})
  }

  @action
  updateAgent(call){
    this.agents.forEach((agent) => { 
      if (call.destination === agent.ext) {
      
      agent.currentCall = call

    }})
  }
  
  @action
  updateCalls(call) {
    let found = false
    this.calls.forEach(c => { 
      if (c.ucid===call.node.ucid) {
      
      c.update(call.node)
      //c = new CallModel(call.node, this)
      
      this.updateQueue(c)
      this.updateAgent(c)
      found = true

    }
  })

  if (found === false) {
    let c = new CallModel(call.node, this)
    this.calls.push(c)
    

  this.updateQueue(c)
  this.updateAgent(c)
}
//this.updateQueue(call.node)
//  this.updateAgent(call.node)
  return true

  }

  @action
  async GetAgentList() {
    this.ds.ListAgents().then((data) => this.onListRecieved(data))
  }

  @action
  async GetQueuesList() {
    this.ds.getQueueLines().then((data) => this.onQueuesRecieved(data))
  }
  @action
  async GetQueuesUpdates() {
    this.getActiveCalls()
    //this.ds.getQueueLines().then((data) => this.onQueuesUpdateRecieved(data))
  }

  

  onQueuesUpdateRecieved(data) {

    var listofqueues = [];
    if (data.data.allAgents) { listofqueues = data.data.allAgents.edges.map((edge) => { return edge.node }) }
    for (let i = 0; i < this.queues.length; i++) {
      listofqueues.forEach((queue) => {
        if (queue.ext === this.queues[i].ext) {


          if (queue.currentCall) {
            
            //this.queues[i].updateCall(queue.currentCall.ucid)
            this.queues[i].currentCall.update(queue.currentCall)
            //this.queues[i].currentCall = { callType: queue.currentCall.callType, origin: queue.currentCall.origin, start: queue.currentCall.start, ucid: queue.currentCall.ucid }


           // console.log(this.queues[i])

          } else {
            this.queues[i].removeCall()
          }

        }
      })


    }
  }

  onListRecieved(data) {
    var listofusers = [];
    if (data.data.allAgents) { listofusers = data.data.allAgents.edges.map((edge) => { return edge.node }) }
    this.agents = []
    listofusers.map((user) => this.addAgent(user))
    //this.setState( { serverData : { users : users.users } }
  }



  onQueuesRecieved(data) {
    var listofqueues = [];
    if (data.data.allAgents) { listofqueues = data.data.allAgents.edges.map((edge) => { return edge.node }) }
    this.queues = []
    listofqueues.map((queue) => this.addQueue(queue))
    //this.setState( { serverData : { users : users.users } }
  }

  @action
  addQueue(queue) {

    this.queues.push(new AgentModel(queue, this))
  }


  @action
  async GetAgent(login) {
    this.ds.GetAgent(login).then((data) => this.onAgentRecieved(data))

  }



  onAgentRecieved(data) {
    var listofusers = [];
    if (data.data.allAgents) { listofusers = data.data.allAgents.edges.map((edge) => { return edge.node }) }
    //var users = { users : listofusers }
    if (listofusers.length === 1) {
      let found = false;
      for (let i = 0; i < this.agents.length; i++) {
        if (listofusers[0].phoneLogin === this.agents[i].phoneLogin) {
          let agent = new AgentModel(listofusers[0], this)
          this.agents[i] = agent
          found = true;
        }
      }
        if (found === false) {
          this.addAgent(new AgentModel(listofusers[0],this))
       
      }
    }
    //this.setState( { serverData : { users : users.users } }
  }


}

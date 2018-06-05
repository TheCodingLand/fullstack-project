import { observable, computed, action } from "mobx";
import AgentModel from "./AgentModel";
import CallModel from "./CallsModel";

//actions:
//calls : newcall, phonenumber, calltype, transfer, endcall
//agents : login, logoff, changestate, linkcall

export default class AgentListModel {
  constructor(ds) {
    this.ds = ds
    
  }
  @observable calls= []
  @observable queues = []
  @observable agents = []

  currentUser = {}

  getActiveCalls(){
    this.ds.getActiveCalls().then((calls) => {calls.data.allCalls.edges.map(call => { return new CallModel(call.node, this) })}).then(calls => this.calls = calls)
  }

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
      console.log(`transfer detected for ${data.data}, call : ${data.id}`)
      this.GetQueuesUpdates().then(() => {
      for (let i = 0; i < this.agents.length; i++) {
        if (data.data === this.agents[i].phoneLogin) {
          this.agents[i].updateCall(data.id)
        }
      }})
    }

 /*    if (data.action === "transferring") {
      for (let i = 0; i < this.agents.length; i++) {
        if (data.data === this.agents[i].phoneLogin) {
          this.GetAgent(data.data)
          data.
        }
      }
    } */

    if (data.action === "endcall") {
      console.log(`call end detected for ${data.data}, call : ${data.id}`)
      this.GetQueuesUpdates().then(() => {
      for (let i = 0; i < this.agents.length; i++) {
        if (data.data === this.agents[i].phoneLogin) {
          this.agents[i].removeCall()
          this.agents[i].updateState(data.data)
        }
      }
    }
  )
    }

    if (data.action === "create") {
      console.log(`detected create call ${data.id}`)
      this.GetQueuesUpdates()
    }
    if (data.action === "calltype") {
      this.GetQueuesUpdates()
    }
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
    
  }

  @action
  addAgent(agent) {

    this.agents.push(new AgentModel(agent, this))
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
    this.ds.getQueueLines().then((data) => this.onQueuesUpdateRecieved(data))
  }


  onQueuesUpdateRecieved(data) {

    var listofqueues = [];
    if (data.data.allAgents) { listofqueues = data.data.allAgents.edges.map((edge) => { return edge.node }) }
    for (let i = 0; i < this.queues.length; i++) {
      listofqueues.forEach((queue) => {
        if (queue.ext === this.queues[i].ext) {


          if (queue.currentCall) {
            //this.queues[i].updateCall(queue.currentCall.ucid)
            this.queues[i].currentCall = { callType: queue.currentCall.callType, origin: queue.currentCall.origin, start: queue.currentCall.start, ucid: queue.currentCall.ucid }


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

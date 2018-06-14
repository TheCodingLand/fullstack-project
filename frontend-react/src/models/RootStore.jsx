import AgentListModel from './AgentListModel'
import io from 'socket.io-client';
import DataProvider from './../DataProvider'


export default class RootStore {
    
    constructor() {
    console.log("Loading root store")
    let SOCKET_URL = "ws.lbr.lu"
    this.ds = new DataProvider();  
    this.socket = io.connect(SOCKET_URL);
    this.agentStore = new AgentListModel(this.ds, this.socket)
    this.pendingUpdates=[]
    this.lastupdate = {}
    
   
    

    this.socket.on('message',((data) =>  { this.handleRedisMessage(data)  }))  
        
    //pl: "{ "item" : "call", "action" : "endcall", "id" : "5781528099517912", "data" : "109" }"}
    
    }

    updatePendingTickets(id){
        this.socket.send("updatetickets:"+ id)
    }

    
    alreadyUpdating(data){
        let updating = false

        for(var i=0; i < this.pendingUpdates.length; i++) {
            let d = this.pendingUpdates[i]
        if (d.action === data.action && d.data === data.data && d.id === data.id && d.item === data.item){      
           
        updating = true 
        }
    
    
    }
    return updating
}   


    handleRedisMessage(data){

        data = data.pl.replace('\\"', '"')
        data = JSON.parse(data)
        data = {action : data.action, data : data.data, id: data.id, item : data.item}
        
        let d = this.lastupdate

        if (d.action === data.action && d.data === data.data && d.id === data.id && d.item === data.item){     }
        else{

        
        if (this.alreadyUpdating(data) === false) {
            this.lastupdate=data
            this.pendingUpdates.push(data)
            this.agentStore.handleMessage(data).then(() => { this.pendingUpdates= this.pendingUpdates.filter((d) => { return d !== data })})
            
        }}

     
    }
}


         




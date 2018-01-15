import AgentListModel from './AgentListModel'
import io from 'socket.io-client';
import CallsListModel from './CallsListModel'

import DataProvider from './../DataProvider'

export default class RootStore {
    constructor() {
    this.lastUpdate = Date.now(); 
    this.lastRedisUpdate = {}
    let SOCKET_URL = "148.110.107.15:3001"
    this.ds = new DataProvider();  

    this.agentStore = new AgentListModel(this)
    this.callsStore = new CallsListModel(this)

    this.socket = io.connect(SOCKET_URL);
    this.socket.on('message',((data) =>  { this.handleRedisMessage(data)})  );
    
    }

    handleRedisMessage(data){
        data = data.pl.replace('\\"', '"')
        data = JSON.parse(data)
        if (data.action === this.lastRedisUpdate.action && data.data === this.lastRedisUpdate.data) {
            if (Date.now() - this.lastUpdate > 2000) {
                
                this.agentStore.handleMessage(data)
                this.lastUpdate = Date.now()
                this.lastRedisUpdate = data
            }
        }
        else {
            this.lastRedisUpdate = data
            this.lastUpdate = Date.now()
            this.agentStore.handleMessage(data)
            
        }
     } 
        }




  
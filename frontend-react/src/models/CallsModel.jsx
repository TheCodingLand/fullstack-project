export default class CallModel {
    constructor(call,rootstore) {

    this.ds = rootstore.ds
      
    
    this.ucid = call.ucid
    this.origin = call.origin
    this.start = call.start
    this.destination = call.destination
    this.callType = call.callType
    
    }

    getClientTickets()
    {

    }

    
}

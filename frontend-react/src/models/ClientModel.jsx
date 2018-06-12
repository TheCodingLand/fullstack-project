


export default class ClientModel {
    constructor(client) {

    
      
    this.otId = client.id
    this.FirstName = client.data.FirstName
    this.LastName = client.data.LastName
    console.log("found client : " + this.FirstName + " " + this.LastName)
    

    
    

    
    

    }

    
}



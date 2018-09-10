import Client from './ClientModel'
import { action } from 'mobx';
import { observable } from "mobx";

export default class CallModel {
    @observable possibleClients
    @observable destination
    @observable callType
    constructor(call, rootstore) {
        if (call.origin) {
            if (call.origin.charAt(0) === '0') {
                this.origin = call.origin.substr(1);
            }
            else {
                this.origin = call.origin
            }
        }
        if (call.destination) {
            if (call.destination.charAt(0) === '0') {
                this.destination = call.destination.substr(1);
            }
            else {
                this.destination = call.destination
            }
        }

        this.ucid = call.ucid
        this.start = call.start
        this.callType = call.callType
        this.possibleClients = []
        this.getPossibleClients()

    }

    update(call) {

        if (call.origin) {
            if (call.origin.charAt(0) === '0') {
                this.origin = call.origin.substr(1);
            }
            else {
                this.origin = call.origin
            }
        }
        if (call.destination) {
            if (call.destination.charAt(0) === '0') {
                this.destination = call.destination.substr(1);
            }
            else {
                this.destination = call.destination
            }
        }

        this.ucid = call.ucid
        this.start = call.start
        this.callType = call.callType
    
    }

   
    @action
    getPossibleClients() {



        let query = {

            objectclass: "Client",
            filter: "ClientFromPhone",
            variables: [
                {
                    name: "phone",
                    value: this.origin

                    //value: "4634637941"
                }
            ],
            requiredfields: [
            ]
        }
        //console.log(query)
        return fetch('http://ticketsadmin.lbr.lu/api/ot/objects', {
            method: 'POST',
            body: JSON.stringify(query),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }
        ).then(response => response.json()
        ).then(
            (response) => {
                if (response.status === "success") {
                    //console.log(response.Client)

                    let clients = response.Client.map((client) => { return new Client(client) })
                    this.possibleClients = clients
                }
                else {
                    this.possibleClients = []
                }
            }
        )
    }
}

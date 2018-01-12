export default class CallModel {

@observable ucid;
@observable origin;
@observable start;
@observable call_type;
@observable destination;


constructor(call) {
    this.ucid=call.ucid
    this.origin=call.origin
    this.start=call.start
    this.call_type=call.call_type
    this.destination=call.destination

}


}
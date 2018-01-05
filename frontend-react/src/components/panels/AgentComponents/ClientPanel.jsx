import * as React from 'react';

// let defaultStyle = { 
//     color : '#fff' 
//   };



export default class ClientPanel extends React.Component {

    render () {
      let call;
      if (this.props.user.currentCall) {
        if (this.props.user.currentCall.origin) {
          call =<div><h3>{this.props.user.currentCall.origin}</h3><h3>{this.props.user.currentCall.callType}</h3></div>
        }
        else{
          call = <h3>no calls</h3>
        }
      }
      
      
      return(call ?
        <div style={{display : 'inline-block'}}>{call} </div> :
        <h3>NoCalls</h3>
        ); 
    }
  }
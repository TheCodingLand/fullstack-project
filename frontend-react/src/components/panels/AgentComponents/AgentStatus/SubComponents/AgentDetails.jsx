import * as React from 'react';
import './agentstyle.css';
// let defaultStyle = { 
//     color : '#fff' 
//   };
export default class AgentDetails extends React.Component {
    render () {
      let classname = this.props.user.phoneState === "ACDAVAIL" ? "agentactive" : "agentinactive";
      return(this.props.user ? 
        <div style={{display : 'inline-block'}} className={classname}>
          <h3> AgentDetails : {this.props.user.firstname}</h3>
          <h3> AgentPhone : {this.props.user.ext}</h3>
        </div> :
        <h3>loading users</h3>
      ); 
    }
  }